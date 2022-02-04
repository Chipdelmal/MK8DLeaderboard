
from datetime import date
from random import shuffle
from os import path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pylab as ply

FNAME = 'leadRunsHistoryBkp.csv'
OUT = '/home/chipdelmal/Documents/MK8D/Leaderboard/'
###############################################################################
# Read file
###############################################################################
df = pd.read_csv(path.join(OUT, FNAME))
###############################################################################
# Cleaning columns
###############################################################################
df['Runner'] = [str(i) for i in df['Runner']]
df['Date'] =  pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.date
df['Submitted in'] =  pd.to_datetime(df['Submitted'], format='%Y-%m-%d').dt.date
df['Time'] = pd.to_timedelta(df['Time'])
###############################################################################
# Getting variables for processing
###############################################################################
elms = (df['Date'], df['Runner'], df['Time'])
(datesUQ, namesUQ, timesUQ) = [sorted(list(i.unique())) for i in elms]
(datesNUM, namesNUM, timesNUM) = [len(i) for i in (datesUQ, namesUQ, timesUQ)]
###############################################################################
# Processing
###############################################################################
dte = datesUQ[-1]
# Get all entries before a given date
dfSub = df[df['Date'] <= dte]
dfPiv = dfSub.pivot_table(
    index='Runner', columns='Date', values='Time', aggfunc='first'
)
dfPiv = dfPiv.reset_index().set_index('Runner')
dfTrs = dfPiv.transpose()
dfPad = dfTrs.fillna(
    value=None, method='ffill', axis=None, 
    inplace=False, limit=None, downcast=None
).transpose()
dfRnk = dfPad.rank(ascending=True, method='first', axis=0)
###############################################################################
# Plots Ranks
###############################################################################
aspect = .3
colors = ply.cm.BuPu(np.linspace(0, 1, namesNUM))
shuffle(colors)
font = {'color':  '#00000022', 'weight': 'normal', 'size': 45,}
dates = list(dfRnk.columns)
# Ranks Plot ------------------------------------------------------------------
(fig, ax) = plt.subplots(1, 1, figsize=(15, 3.5))
for i in range(namesNUM):
    if dfRnk.iloc[i].name == 'chipdelmal':
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
# Styling ---------------------------------------------------------------------
ax.hlines(
    [10, 25, 50, 100, 150, 200, 250], 
    xmin=dates[0], xmax=dates[-1],
    lw=.5, alpha=.5, ls='--', color='k', zorder=5
)
vLines = [date(i, 1, 1) for i in range(dates[0].year, dates[-1].year+1)]
ax.vlines(
    vLines, ymin=0, ymax=namesNUM,
    lw=.5, alpha=.5, ls='--', color='k', zorder=5
)
for dPos in vLines[1:]:
    ax.text(
        dPos, namesNUM/2, dPos.year, rotation=90,
        horizontalalignment='right', verticalalignment='center',
        fontdict=font, zorder=-5
    )
# Axes ------------------------------------------------------------------------
ax.set_title("Mario Kart 8 Deluxe's Leaderboard History", fontsize=30)
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Rank", fontsize=20)
fmt_month = mdates.MonthLocator((1, 4, 10))
ax.xaxis.set_minor_locator(fmt_month)
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.tick_params(axis="x", which="both", rotation=0)
ax.margins(x=0); ax.margins(y=0)
ax.set_xlim(dates[0], dates[-1])
ax.set_ylim(0, namesNUM)
ax.set_aspect(aspect/ax.get_data_ratio())
# Export ----------------------------------------------------------------------
fig.savefig(
    path.join(OUT, 'leadRanks.png'), dpi=750, bbox_inches="tight",
    facecolor='w'
)
###############################################################################
# Plots Scaled
###############################################################################
highName = 'chipdelmal'
(fg, bg, aspect) = ('#3a0ca320', '#f7258599', .3)
tScale = (1e9*60)
# Plot
(fig, ax) = plt.subplots(figsize=(15,15))
for name in namesUQ:
    dfSub = df[df['Runner']==name]
    if name!='chipdelmal':
        ax.plot(
            dfSub['Date'], dfSub['Time']/tScale, 
            color=fg, marker='o', ms=0, lw=2, zorder=1,
            dash_capstyle='round', dash_joinstyle='round'
        )
dfSub = df[df['Runner']==highName]
# ax.plot(dfSub['Date'], dfSub['Time']/tScale, color=bg, zorder=5)
ax.plot(
    dfSub['Date'], dfSub['Time']/tScale, 
    color=bg, marker='o', ms=0, lw=2.5, zorder=10,
    dash_capstyle='round', dash_joinstyle='round'
)
# Styling
ax.margins(x=0)
ax.margins(y=0)
ax.set_ylim(80, 120)
ax.set_aspect(aspect/ax.get_data_ratio())
fig.savefig(
    path.join(OUT, 'leadTraces.png'),
    dpi=500, pad_inches=.1
)
plt.close('all')
###############################################################################
# Debugging
###############################################################################
minT = min(df['Time'])
df[df['Time']==minT]