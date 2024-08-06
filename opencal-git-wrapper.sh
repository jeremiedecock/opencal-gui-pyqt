#!/bin/bash

DATA_GIT_PATH=~/data_opencal
LAUNCH_SCRIPT_PATH=~/bin/opencal
LOG_PATH=~/data_opencal/timemg-opc.csv  # TIME MG TIME TRACKER
BACKUP_SCRIPT_PATH=~/bin/opencal-backup
DUMP_SCRIPT_PATH=~/bin/opencal-dump
RESTORE_SCRIPT_PATH=~/bin/opencal-restore
XML_TO_SQLITE_SCRIPT_PATH=~/bin/opencal-xml-to-sqlite

echo ""
echo "Shortkeys:"
echo "- Answer action: ............... Space            ('Fullscreen' on remote controls)"
echo "- Skip card action: ............ CTRL + Space"
echo "- Skip level action: ........... CTRL + PageUp    ('Echap' on remote controls)"
echo "- Hide card action: ............ SHIFT + Space"
echo "- Right answer action: ......... L                ('>' on remote controls)"
echo "- Wrong answer action: ......... H                ('<' on remote controls)"
echo "- Right answer action + hide: .. SHIFT + L"
echo "- Wrong answer action + hide: .. SHIFT + H"
echo ""

if [ -e ~/opencal.lock ]
then
    zenity --error --title="Error" --text="OPC already run (~/opencal.lock)"
else
    touch ~/opencal.lock

    echo ""
    echo "Synchronizing data..."

    # TODO: WORKAROUND https://forum.qt.io/topic/54802/linux-application-does-not-accept-keyboard-input/4
    #QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb $OPC

    # Try to pull the latest changes from the git repository
    git -C ${DATA_GIT_PATH} pull 2> git_error.txt
    if [ $? -ne 0 ]
    then
        echo "Git Pull Error: $(cat git_error.txt)"
        # If git pull fails, display the error message and wait for user confirmation
        zenity --error --title="Git Pull Error" --text="$(cat git_error.txt)"
        rm git_error.txt
    else
        # Make the SQLite database from the fetched opencal.sql file
        ${RESTORE_SCRIPT_PATH}

        echo ""
        echo "opc-start,$(date --iso-8601='seconds')" >> ${LOG_PATH}  # TIME MG TIME TRACKER

        # If git pull succeeds, execute the launch script
        ${LAUNCH_SCRIPT_PATH}

        echo "opc-stop,$(date --iso-8601='seconds')" >> ${LOG_PATH}  # TIME MG TIME TRACKER
        echo ""

        # Execute the backup and dump scripts
        #${XML_TO_SQLITE_SCRIPT_PATH}          # This is commented out because consolidation reviews have a different ID at each import then git diffs are always huge
        ${BACKUP_SCRIPT_PATH}
        ${DUMP_SCRIPT_PATH}
        xz -vv --force ${DATA_GIT_PATH}/*_opencal.sqlite

        # Try to pull the latest changes from the git repository
        git -C ${DATA_GIT_PATH} status

        # Print git diff
        git -C ${DATA_GIT_PATH} diff

        # Ask for user confirmation to do a git commit+push
        if zenity --question --title="Git Push" --text="Do you want to push changes to the remote repository?"
        then
            # If user's answer is positive, commit changes and push to the origin remote repository
            git -C ${DATA_GIT_PATH} add jeremie.pkb opencal_config.yml opencal.sql timemg-opc.csv assets/*
            git -C ${DATA_GIT_PATH} commit -m "Up."
            git -C ${DATA_GIT_PATH} push
        fi
    fi

    rm ~/opencal.lock

    # Wait for user confirmation to close the terminal (to read the error message if any)
    read -p "Press [Enter] to close the terminal..."
fi
