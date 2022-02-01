
from os import path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

FNAME = 'leadRunsHistory.csv'
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
dte = datesUQ[3]
# Get all entries before a given date
dfSub = df[df['Date']<=dte]
###############################################################################
# Plots
###############################################################################
highName = 'chipdelmal'
(fg, bg, aspect) = ('#3a0ca322', '#f7258577', .3)
tScale = (1e9*60)
# Plot
(fig, ax) = plt.subplots(figsize=(15,15))
for name in namesUQ:
    dfSub = df[df['Runner']==name]
    if name!='chipdelmal':
        ax.plot(
            dfSub['Date'], dfSub['Time']/tScale, 
            color=fg, marker='o', ms=1, lw=1, zorder=1,
            dash_capstyle='round', dash_joinstyle='round'
        )
dfSub = df[df['Runner']==highName]
# ax.plot(dfSub['Date'], dfSub['Time']/tScale, color=bg, zorder=5)
ax.plot(
    dfSub['Date'], dfSub['Time']/tScale, 
    color=bg, marker='o', ms=1.25, lw=1, zorder=10,
    dash_capstyle='round', dash_joinstyle='round'
)
# Styling
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