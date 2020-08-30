
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import gridspec


(IN, FILE, OUT) = ('./out/', '2020-08-29_200cc_NoItems.csv', './img/')
# Read dataframe --------------------------------------------------------------
ldBrd = pd.read_csv(IN+FILE)
colors = ['#1344b8', '#ed174b']
palette = sns.set_palette(colors)
# #############################################################################
# Plots
# #############################################################################
(dFlt, cFlt) = (ldBrd['Version'] == 'Digital', ldBrd['Version'] == 'Cartridge')
(dTimes, cTimes) = (ldBrd[dFlt]['Time'], ldBrd[cFlt]['Time'])
# (fig, (axt, ax, axb)) = plt.subplots(3, 1, sharex=True, figsize=(6, 2))
fig = plt.figure(figsize=(18, 8))
spec = gridspec.GridSpec(3, 1, height_ratios=[.5, 1, .5], hspace=0)
axb = fig.add_subplot(spec[0])
ax = fig.add_subplot(spec[1])
axt = fig.add_subplot(spec[2])
# Violin plot #################################################################
ax = sns.violinplot(
        y=["Attempts"]*len(ldBrd), x='Time', hue="Version",
        data=ldBrd, palette=palette, split=True, ax=ax,
        cut=0, orient="h", saturation=.75, inner=None, linewidth=.1
    )
# Post Plot -------------------------------------------------------------------
handles, _ = ax.get_legend_handles_labels()
(minT, maxT) = (min(list(ldBrd["Time"])), max(list(ldBrd["Time"])))
(pRange, height) = ((minT-minT*.01, maxT+maxT*.01), .5)
ax.legend(handles, ["D", "C"])
ax.hlines(
        [0], xmin=pRange[0], xmax=pRange[1],
        colors='k', linewidth=.5, ls='dashed'
    )
ax.vlines(dTimes, ymin=-height, ymax=0, colors=colors[0], linewidth=.2)
ax.vlines(cTimes, ymin=0, ymax=height, colors=colors[1], linewidth=.2)
for violin, alpha in zip(ax.collections[:2], [.2, .2]):
    violin.set_alpha(alpha)
ax.set_ylim(-height, height)
# Labels and limits  ----------------------------------------------------------
ax.set_xlim(*pRange)
ax.legend_.remove()
ax.set_yticklabels('')
# Histograms ##################################################################
rowNum = ldBrd.shape[0]
bins = round(rowNum / 2)
hi = 8
axt = sns.distplot(
        ldBrd[dFlt].get('Time'),
        bins=bins, kde=False, color=colors[0], ax=axt
    )
axb = sns.distplot(
        ldBrd[cFlt].get('Time'),
        bins=bins, kde=False, color=colors[1], ax=axb
    )
for p in axt.patches:
    p.set_height(-p.get_height())
axb.set_ylim(0, hi)
axt.set_ylim(-hi, 0)
axt.set_xlim(*pRange)
axb.set_xlim(*pRange)
# #############################################################################
# Save
# #############################################################################
fig.savefig(OUT+'violin.png', dpi=500, bbox='tight', pad_inches=.1)
