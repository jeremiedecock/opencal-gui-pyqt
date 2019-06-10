#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opencal.core.data import card_list_to_dataframes

import numpy as np

import pandas as pd
import datetime
import matplotlib.dates as mdates

import math

from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#import seaborn as sns

from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU

BLUE = '#1f77b4'
RED = '#d62728'
YELLOW = '#ff7f0e'
GREEN = '#2ca02c'


def plot_card_addition(df, ax):
    #tk1 = list(reversed(-np.arange(0, -df.wushift.min(), 30)))
    #tk2 = list(np.arange(0, df.wushift.max(), 30))

    try:
        df.loc[df.cdate > datetime.datetime.now() - datetime.timedelta(days=30)].groupby("cdate").hidden.count().plot(x='cdate',
                                                                                                                    y='hidden',
                                                                                                                    kind='bar',
                                                                                                                    color=BLUE,
                                                                                                                    #yticks=tk1 + tk2,
                                                                                                                    ax=ax)
    except TypeError as e:
        pass

    # set locator
    #self.ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
    ##self.ax2.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

    # set formatter
    ##self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%a %d-%m'))
    #self.ax2.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))

    # set font and rotation for date tick labels
    #self.fig.autofmt_xdate()

    ax.grid(True, axis="y", linestyle=':', alpha=0.75)

    ax.set_title("Card addition")
    ax.set_xlabel("")
    ax.set_ylabel("Number of cards")

    if ax.get_legend() is not None:
        ax.get_legend().remove()


def plot_card_review(df, ax):
    #tk1 = list(reversed(-np.arange(0, -df.wushift.min(), 30)))
    #tk2 = list(np.arange(0, df.wushift.max(), 30))

    df.loc[df.rdate > datetime.datetime.now() - datetime.timedelta(days=30)].groupby("rdate").result.count().plot(x='rdate',
                                                                                                                  y='result',
                                                                                                                  kind='bar',
                                                                                                                  color=BLUE,
                                                                                                                  #yticks=tk1 + tk2,
                                                                                                                  ax=ax)

    ax.grid(True, axis="y", linestyle=':', alpha=0.75)

    ax.set_title("Card review")
    ax.set_xlabel("")
    ax.set_ylabel("Number of cards")

    if ax.get_legend() is not None:
        ax.get_legend().remove()


class PlotCanvas(FigureCanvas):
    """This is a Matplotlib QWidget.

    See https://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
    """

    def __init__(self, card_list, parent, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        nrows = 1
        ncols = 2
        self.ax1 = self.fig.add_subplot(nrows, ncols, 1)
        self.ax2 = self.fig.add_subplot(nrows, ncols, 2)

        self.card_list = card_list

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def compute_initial_figure(self):
        self.update_figure(init=True)


    def update_figure(self, init=False):

        if not init:
            self.ax1.cla()
            self.ax2.cla()

        try:
            card_df, review_df = card_list_to_dataframes(self.card_list)

            #df['date_fmt'] = df['date'].dt.strftime('%a %d/%m')
            #df.loc[::2, 'date_fmt'] = ''

            ###################################

            plot_card_addition(card_df, self.ax1)

            plot_card_review(review_df, self.ax2)

            ###################################

            self.fig.tight_layout()
            
        except IndexError as e:
            # Happen when data is empty
            print(e)
            #pass

        if not init:
            self.draw()
