
from collections import OrderedDict
from os import path
from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from dateutil import parser
from random import shuffle
from random import uniform



def getPlayerRanks(name, boards):
    (ranks, times) = ([], [])
    for brd  in boards:
        row = brd[brd['Player']==name]
        if row.shape[0] > 0:
            (rank, time) = (
                row['Rank'].values[0], 
                row['Time'].values[0]
            )
        else:
            (rank, time) = (np.nan, np.nan)
        ranks.append(rank)
        times.append(time)
    return (ranks, times)


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
    (ranks, times) = getPlayerRanks(name, ldBrds)
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
subset = (0, len(names))
xCoords = [(i-fdates[0]).days for i in fdates]
nme = list(names)[0]
colors = pl.cm.plasma(np.linspace(0, 1, subset[1]-subset[0]))
shuffle(colors)
(fig, ax) = plt.subplots(1, 1, figsize=(12, 12/2))
for (ix, nme) in enumerate(list(names)[subset[0]:subset[1]]):
    plt.plot(
        xCoords, entries[nme], # [0 if x is np.nan else x for x in entries[nme]],
        lw=.75, alpha=.75, color=colors[ix],
        marker='.', markersize=0,
        #solid_joinstyle='round',
        #solid_capstyle='butt'
    )
ax.vlines(
    xCoords, 0, 1, 
    transform=ax.get_xaxis_transform(),
    lw=0.1, color='b'
)
ax.hlines(
    list(range(subset[0]+1, subset[1], 5)), 0, 1, 
    transform=ax.get_yaxis_transform(),
    lw=0.1, color='b'
)
fig.savefig("./test", dpi=500)
# ax.set_facecolor('k')




###############################################################################
# Debug
###############################################################################
# i=30
# fnames[i]
# ldBrds[i]
# [ix for (ix, i) in enumerate(times) if i == 109.7]