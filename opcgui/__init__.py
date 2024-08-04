"""OpenCAL GUI

Opencal Python GUI

Note:

    This project is in beta stage.

Viewing documentation using IPython
-----------------------------------
To see which functions are available in `opcgui`, type ``opcgui.<TAB>`` (where
``<TAB>`` refers to the TAB key), or use ``opcgui.*get_version*?<ENTER>`` (where
``<ENTER>`` refers to the ENTER key) to narrow down the list.  To view the
docstring for a function, use ``opcgui.get_version?<ENTER>`` (to view the
docstring) and ``opcgui.get_version??<ENTER>`` (to view the source code).
"""

import importlib.metadata
import opcgui.path

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
# X.Y
# X.Y.Z # For bugfix releases  
# 
# Admissible pre-release markers:
# X.YaN # Alpha release
# X.YbN # Beta release         
# X.YrcN # Release Candidate   
# X.Y # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
#

__version__ = importlib.metadata.version("opcgui")

def get_version():
    return __version__

APPLICATION_NAME = "OpenCAL"

__all__ = ['config']


# CONFIGURATION ###############################################################

# from dataclasses import dataclass
# import os
# import yaml

# # Dataclass: c.f. https://docs.python.org/3/library/dataclasses.html and https://stackoverflow.com/questions/31252939/changing-values-of-a-list-of-namedtuples/31253184
# @dataclass
# class Config:
#     pkb_path: str
#     pkb_medias_path: str
#     mathjax_path: str
#     html_scale: float
#     consolidation_professor: str
#     acquisition_professor: str
#     active_list_increment_size: int
#     max_cards_per_grade: int
#     tag_priority_dict: dict
#     tag_difficulty_dict: dict
#     reverse_level_0: bool
#     default_html_base_path: str

# config = None       # The instance that contains the loaded configuration

# def load_config_file(file_path="~/.opencal.yaml"):
#     global config

#     file_path = os.path.expanduser(file_path)  # to handle "~/..." paths
#     file_path = os.path.abspath(file_path)     # to handle relative paths

#     with open(file_path) as stream:
#         config_dict = yaml.safe_load(stream)
#         config = Config(**config_dict)
