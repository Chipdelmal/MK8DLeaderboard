
from collections import OrderedDict
from os import path
from glob import glob
from numpy.lib.arraypad import pad
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from dateutil import parser
from random import shuffle
from random import uniform
import plotly.express as px
import matplotlib.pylab as ply
import plotly.graph_objects as go
import functions as fun
from datetime import datetime, timedelta



(IN, FILE, OUT) = (
    '/home/chipdelmal/Documents/MK8D/Leaderboard/',
    '*_48_200cc_NoItems.csv',
    '/home/chipdelmal/Documents/MK8D/Leaderboard/img/'
)
fnames = sorted(glob(path.join(IN, FILE)))
fdates = [parser.parse(path.split(i)[-1][:10]) for i in fnames]
###############################################################################
# Process
###############################################################################
ldBrds = [pd.read_csv(i) for i in fnames]
namesLst = [i['Player'].unique() for i in ldBrds]
names = list(set(x for lst in namesLst for x in lst))
# Get players dictionaries ----------------------------------------------------
playersDicts = {}
name = 'Pianist15'
for name in names:
    (ranks, times) = fun.getPlayerRanks(name, ldBrds)
    meanRank = np.nanmean(ranks)+uniform(0, 0.01)
    playersDicts[meanRank] = {
        'Name': name, 'Ranks': ranks, 'Times':times
    }
###############################################################################
# Re-shape in order
###############################################################################
sortedRanks = sorted(list(playersDicts.keys()))
entries = {
    playersDicts[ix]['Name']: playersDicts[ix]['Ranks']
    for ix in sortedRanks
}
names = entries.keys()
# Plot ------------------------------------------------------------------------
hlight = set(['chipdelmal'])
subset = (0, len(names))
xCoords = [(i-fdates[0]).days for i in fdates]
nme = list(names)[0]
rvb = fun.colorPaletteFromHexList([
    '#ff0054', '#ff5c8a', '#8338ec', '#70d6ff', '#03045e'
])
colors = rvb(np.linspace(0, 1, num=20))
# colors = ply.cm.Pastel1(np.linspace(0, 1, num=20))
# colors = list(colors)*len(names)
# colors = pl.cm.seismic(np.linspace(0, 1, num=20))# subset[1]-subset[0]))
colors = list(colors)*len(names)
shuffle(colors)
(fig, ax) = plt.subplots(1, 1, figsize=(12, 12/2))
for (ix, nme) in enumerate(list(names)[subset[0]:subset[1]]):
    color = colors[ix]
    if nme in hlight:
        color = 'k'
    plt.plot(
        xCoords, entries[nme], # [0 if x is np.nan else x for x in entries[nme]],
        lw=.45, alpha=.75, color=color,
        marker='.', markersize=0,
        solid_joinstyle='round',
        solid_capstyle='butt'
    )
ax.vlines(
    xCoords, 0, 1, 
    transform=ax.get_xaxis_transform(),
    lw=0.25, color=(0, 0, 1, .5)
)
ax.hlines(
    list(range(subset[0], subset[1], 10)), 0, 1, 
    transform=ax.get_yaxis_transform(),
    lw=0.25, color=(0, 0, 1, .5)
)
ax.set_xlim(0, max(xCoords))
ax.set_ylim(0, max(ldBrds[-1]['Rank'])+1)
ax.set_aspect((1/4)/ax.get_data_ratio())
# ax.set_xticks(xCoords)
# ax.set_xticklabels([x.strftime('%Y-%m-%d') for x in fdates])
ax.set_xticks(range(0, xCoords[-1], 15))
ax.set_xticklabels([(fdates[0]+timedelta(x)).strftime('%Y-%m-%d') for x in range(0, xCoords[-1], 15)])
plt.xticks(rotation=90)
# plt.xlabel('Date')
# plt.xlabel('Date (Y-M-D)', size=30)
plt.ylabel('Rank', size=30)
ax.set_facecolor('w')
fig.savefig(path.join(OUT, 'RanksHistory.png'), dpi=750)
###############################################################################
# Interactive
###############################################################################
alpha=.5
fig = go.Figure()
for (ix, nme) in enumerate(list(names)[subset[0]:subset[1]]):
    colors[ix][-1]=alpha
    fig.add_trace(
        go.Scatter(
            x=xCoords, y=entries[nme],
            mode='lines', name=nme,
            line = dict(
                color='rgba'+str(tuple(colors[ix])), 
                width=2.5
            )
        )
    )
fig.show()
fig.write_html(path.join(OUT, 'RanksHistory.html'))
###############################################################################
# Debug
###############################################################################
# i=1
# fnames[i]
# list(ldBrds[i]['Rank'])[50:75]
# [ix for (ix, i) in enumerate(times) if i == 109.7]
