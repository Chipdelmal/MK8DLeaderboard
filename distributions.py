
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams["font.family"]="TakaoPGothic"

(IN, FILE, OUT) = (
    '/home/chipdelmal/Documents/MK8D/Leaderboard/',
    '2021-07-05_48_200cc_NoItems.csv',
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
# #############################################################################
# Plots
# #############################################################################
fig = plt.figure(figsize=(25, 4))
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
(pA, pB) = (.025, .975)
(cA, cB) = ([0, 0], [0, 0])
delta = .45
for i in range(entries):
    if list(cFlt)[i]:
        if top:
            if cA[0] == 0:
                (yPos, yAlign) = (pA + cA[0], 'top')
            else:
                (yPos, yAlign) = (pA + cA[0], 'bottom')
            cA[0] = cA[0] + delta
            if cA[0] >= delta + .1:
                cA[0] = 0
        else:
            if cA[1] == 0:
                (yPos, yAlign) = (pB - cA[1], 'bottom')
            else:
                (yPos, yAlign) = (pB - cA[1], 'top')
            cA[1] = cA[1] + delta
            if cA[1] >= delta + .1:
                cA[1] = 0
        top = not top
    else:
        if bot:
            if cB[0] == 0:
                (yPos, yAlign) = (-pA - cB[0], 'bottom')
            else:
                (yPos, yAlign) = (-pA - cB[0], 'top')
            cB[0] = cB[0] + delta
            if cB[0] >= delta + .1:
                cB[0] = 0
        else:
            if cB[1] == 0:
                (yPos, yAlign) = (-pB + cB[1], 'top')
            else:
                (yPos, yAlign) = (-pB + cB[1], 'bottom')
            cB[1] = cB[1] + delta
            if cB[1] >= delta + .1:
                cB[1] = 0
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
    dpi=500, pad_inches=.1
)
