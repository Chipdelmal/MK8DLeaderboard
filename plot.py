
import time
import dateparser
import seaborn as sns
import pandas as pd
import functions as fun
import constants as const
import matplotlib.pyplot as plt


(IN, FILE, OUT) = ('./out/', '2020-08-29_200cc_NoItems.csv', './img/')
# Read dataframe --------------------------------------------------------------
ldBrd = pd.read_csv(IN+FILE)
# Preprocess ------------------------------------------------------------------
rowNum = ldBrd.shape[0]
bins = round(rowNum / 2)
# #############################################################################
# Draft
# #############################################################################
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)
ax2 = sns.violinplot(
        x="Time", y='Version', hue="Version",
        data=ldBrd, palette='seismic', split=True, ax=ax2,
        cut=0
        # scale="count", inner="stick"
    )
ax1 = sns.distplot(
        ldBrd[ldBrd['Version'] == 'Digital'].get('Time'),
        bins=bins, kde=False, color="b", ax=ax1
    )
ax3 = sns.distplot(
        ldBrd[ldBrd['Version'] == 'Cartridge'].get('Time'),
        bins=bins, kde=False, color="r", ax=ax3
    )
for p in ax3.patches:  # turn the histogram upside down
    p.set_height(-p.get_height())
ax1.set_ylim(0, 7.5)
ax3.set_ylim(-7.5, 0)
ax2.legend_.remove()

# Scatter
diffs = []
for dt in ldBrd['Date']:
    today = dateparser.parse('today')
    delta = today - dt
    days = delta.days
    diffs.append(days)

ax4 = plt.scatter(ldBrd['Time'], y=diffs, alpha=0.5)
plt.yscale('log')
# #############################################################################
# Draft
# #############################################################################
(dFlt, cFlt) = (ldBrd['Version'] == 'Digital', ldBrd['Version'] == 'Cartridge')
(dTimes, cTimes) = (ldBrd[dFlt]['Time'], ldBrd[cFlt]['Time'])
# Colors ----------------------------------------------------------------------
colors = ['#ed174b', '#1344b8']
palette = sns.set_palette(colors)
# Plot ------------------------------------------------------------------------
(fig, ax) = plt.subplots(1, 1, sharex=True, figsize=(10, 2))
ax = sns.violinplot(
        y=["Attempts"]*len(ldBrd), x='Time', hue="Version",
        data=ldBrd, palette=palette, split=True, ax=ax,
        cut=0, orient="h", saturation=.75
    )
# Post Plot -------------------------------------------------------------------
handles, _ = ax.get_legend_handles_labels()
(minT, maxT) = (min(list(ldBrd["Time"])), max(list(ldBrd["Time"])))
pRange = (minT-minT*.01, maxT+maxT*.01)
ax.legend(handles, ["D", "C"])
ax.hlines(
        [0], xmin=pRange[0], xmax=pRange[1],
        colors='k', linewidth=.75, ls='dashed'
    )
ax.vlines(dTimes, ymin=-1, ymax=0, colors=colors[0], linewidth=.2)
ax.vlines(cTimes, ymin=0, ymax=1, colors=colors[1], linewidth=.2)
# Save ------------------------------------------------------------------------
ax.set_xlim(*pRange)
ax.legend_.remove()
fig.savefig(OUT+'violin.png', dpi=500)
