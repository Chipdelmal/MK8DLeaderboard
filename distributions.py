
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import gridspec
plt.rcParams["font.family"]="STSong"

(IN, FILE, OUT) = (
    '/home/chipdelmal/Documents/MK8D/Leaderboard/',
    '2020-10-17_48_200cc_NoItems.csv',
    '/home/chipdelmal/Documents/MK8D/Leaderboard/img/'
)
# FILE = sys.argv[1]
# Read dataframe --------------------------------------------------------------
ldBrd = pd.read_csv(IN + FILE)
colors = ['#2D00F7', '#F20089']
palCol = ['#6877f9', '#ed95c7']
palette = sns.set_palette(palCol)
# #############################################################################
# PParse data
# #############################################################################
(dFlt, cFlt) = (ldBrd['Version'] == 'Digital', ldBrd['Version'] == 'Cartridge')
(dTimes, cTimes) = (ldBrd[dFlt]['Time'], ldBrd[cFlt]['Time'])
(nameL, timeL) = [list(i) for i in (ldBrd['Player'], ldBrd['Time'])]

nameL
# #############################################################################
# Plots
# #############################################################################
fig = plt.figure(figsize=(25, 5))
ax = fig.add_subplot()
(minT, maxT) = (min(list(ldBrd["Time"])), max(list(ldBrd["Time"])))
(pRange, height) = ((minT - minT * .01, maxT + maxT * .01), .5)
# Violin plot #################################################################
sns.violinplot(
    y=["Attempts"] * len(ldBrd), x='Time', hue="Version",
    data=ldBrd, palette=palette, split=True, ax=ax,
    cut=0, orient="h", saturation=.85, inner=None, linewidth=0
)
plt.axhline(0, c='k')
# Digital ---------------------------------------------------------------------
for (i, time) in enumerate(dTimes):
    if i % 2 == 0:
        (a, b) = (0, -.5)
    else:
        (a, b) = (-.5, -1)
    ax.vlines([time], a, b, colors=colors[0], lw=1)
# Cartridge -------------------------------------------------------------------
for (i, time) in enumerate(cTimes):
    if i % 2 == 0:
        (a, b) = (0, .5)
    else:
        (a, b) = (.5, 1)
    ax.vlines([time], a, b, colors=colors[1], lw=1)
# Both ------------------------------------------------------------------------
ax.vlines(dTimes, 0, -1, colors=colors[0], lw=.05)
ax.vlines(cTimes, 0, +1, colors=colors[1], lw=.05)
entries = len(nameL)
(top, bot) = (True, True)
for i in range(entries):
    if list(cFlt)[i]:
        if top:
            (yPos, yAlign) = (+0.025, 'top')
        else:
            (yPos, yAlign) = (+0.975, 'bottom')
        top = not top
    else:
        if bot:
            (yPos, yAlign) = (-0.025, 'bottom')
        else:
            (yPos, yAlign) = (-0.975, 'top')
        bot = not bot
    ax.text(
        timeL[i], yPos, str(i + 1) + ': ' + nameL[i],
        fontsize=2.5, rotation=90,
        horizontalalignment='right',
        verticalalignment=yAlign
    )
# #############################################################################
# Save
# #############################################################################
ax.set_xlim(*pRange)
ax.legend_.remove()
ax.set_yticklabels('')
# Save ------------------------------------------------------------------------
fig.savefig(
    OUT + FILE.split('.')[0] + '.png',
    dpi=500, bbox='tight', pad_inches=.1
)
