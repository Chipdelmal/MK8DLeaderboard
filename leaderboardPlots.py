
import numpy as np
from os import path
import pandas as pd
from datetime import date
from random import shuffle
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pylab as ply


(TRK, SPD, ITM) = ('32', '200cc', 'NoItems')
OUT = '/home/chipdelmal/Documents/MK8D/Leaderboard/'
highName = 'chipdelmal'
###############################################################################
# Read file
###############################################################################
dfRnk = pd.read_csv(
    path.join(OUT, 'LeadRanks-{}_{}-{}.csv'.format(TRK, SPD, ITM)), 
    index_col=0
)
(namesNum, datesNum) = dfRnk.shape
# Getting runner's best performance -------------------------------------------
highRow = dfRnk.loc[highName]
highBest = min(highRow[highRow.notna()])
highDate = datetime.strptime(highRow[(highRow==highBest)].index[0], '%Y-%m-%d')
dates = [datetime.strptime(i, '%Y-%m-%d') for i in list(dfRnk.columns)]
###############################################################################
# Plots Ranks
###############################################################################
(aspect, colors, offset) = (.3, ply.cm.BuPu(np.linspace(0, 1, namesNum)), -2.5)
font = {'color':  '#00000022', 'weight': 'normal', 'size': 45,}
shuffle(colors)
buffer = namesNum*.02
# Ranks Plot ------------------------------------------------------------------
(fig, ax) = plt.subplots(1, 1, figsize=(15, 3.5))
for i in range(namesNum):
    if dfRnk.iloc[i].name == highName:
        (color, alpha, zorder) = ('k', .85, 10)
    else:
        (color, alpha, zorder) = (colors[i], .6, 0)
    y = np.asarray(dfRnk.iloc[i])
    plt.plot(
        dates, y,
        lw=.5, alpha=alpha, color=color,
        marker='.', markersize=0,
        solid_joinstyle='round',
        solid_capstyle='round', zorder=zorder
    )
# Highlight the best rank -----------------------------------------------------
# ax.hlines(
#     highBest, xmin=dates[0], xmax=dates[-1],
#     alpha=.5, color='k', zorder=5, lw=.25, #ls=':'
# )
# plt.plot([highDate, highDate], [highBest, highBest+offset], lw=.1)
ax.text(
    highDate, highBest+offset, 
    'Rank: {}\n{}/{:02d}/{:02d}'.format(
        int(highBest), highDate.year, highDate.month, highDate.day
    ), 
    horizontalalignment='center', verticalalignment='top', fontsize=5
)
# Styling ---------------------------------------------------------------------
ax.hlines(
    [10, 25, 50, 100, 150, 200, 250], 
    xmin=dates[0], xmax=dates[-1],
    lw=.35, alpha=.35, ls='--', color='k', zorder=5
)
vLines = [date(i, 1, 1) for i in range(dates[0].year, dates[-1].year+1)]
ax.vlines(
    vLines, ymin=0, ymax=namesNum,
    lw=.35, alpha=.35, ls='--', color='k', zorder=5
)
ax.hlines(
    [0, ], xmin=dates[0], xmax=dates[-1],
    lw=.75, alpha=1, color='#000000', zorder=-5
)
ax.vlines(
    dates, ymin=0-buffer, ymax=0,
    lw=.2, alpha=.75, color='#000000', zorder=-5
)
for dPos in vLines[1:]:
    ax.text(
        dPos, namesNum/2, dPos.year, rotation=90,
        horizontalalignment='right', verticalalignment='center',
        fontdict=font, zorder=-10
    )
# Axes ------------------------------------------------------------------------
ax.set_title("Mario Kart 8 Deluxe's Leaderboard History", fontsize=30)
ax.set_xlabel("Date", fontsize=20); ax.set_ylabel("Rank", fontsize=20)
fmt_month = mdates.MonthLocator((1, 4, 10))
ax.xaxis.set_minor_locator(fmt_month)
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.tick_params(axis="x", which="both", rotation=0)
ax.margins(x=0); ax.margins(y=0)
ax.set_xlim(dates[0], dates[-1]); ax.set_ylim(0-buffer, namesNum)
ax.set_aspect(aspect/ax.get_data_ratio())
# Export ----------------------------------------------------------------------
fig.savefig(
    path.join(OUT, 'LeadRanks-{}_{}-{}.png'.format(TRK, SPD, ITM)), 
    dpi=750, bbox_inches="tight", facecolor='w'
)
###############################################################################
# Plots Scaled
###############################################################################
# highName = 'chipdelmal'
# (fg, bg, aspect) = ('#3a0ca320', '#f7258599', .3)
# tScale = (1e9*60)
# # Plot
# (fig, ax) = plt.subplots(figsize=(15,15))
# for name in namesUQ:
#     dfSub = df[df['Runner']==name]
#     if name!='chipdelmal':
#         ax.plot(
#             dfSub['Date'], dfSub['Time']/tScale, 
#             color=fg, marker='o', ms=0, lw=2, zorder=1,
#             dash_capstyle='round', dash_joinstyle='round'
#         )
# dfSub = df[df['Runner']==highName]
# # ax.plot(dfSub['Date'], dfSub['Time']/tScale, color=bg, zorder=5)
# ax.plot(
#     dfSub['Date'], dfSub['Time']/tScale, 
#     color=bg, marker='o', ms=0, lw=2.5, zorder=10,
#     dash_capstyle='round', dash_joinstyle='round'
# )
# # Styling
# ax.margins(x=0)
# ax.margins(y=0)
# ax.set_ylim(80, 120)
# ax.set_aspect(aspect/ax.get_data_ratio())
# fig.savefig(
#     path.join(OUT, 'leadTraces.png'),
#     dpi=500, pad_inches=.1
# )
# plt.close('all')
