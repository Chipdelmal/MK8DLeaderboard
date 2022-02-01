
from os import path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

FNAME = 'leadRunsHistory_test.csv'
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
df['Submitted in'] =  pd.to_datetime(df['Submitted in'], format='%Y-%m-%d').dt.date
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
(fg, bg, aspect) = ('#3a0ca322', '#f7258599', .3)
tScale = (1e9*60)
# Plot
(fig, ax) = plt.subplots()
for name in namesUQ:
    dfSub = df[df['Runner']==name]
    if name!='chipdelmal':
        ax.plot(dfSub['Date'], dfSub['Time']/tScale, color=fg)
        ax.plot(dfSub['Date'], dfSub['Time']/tScale, color=fg, marker='.')
dfSub = df[df['Runner']==highName]
ax.plot(dfSub['Date'], dfSub['Time']/tScale, color=bg)
ax.plot(dfSub['Date'], dfSub['Time']/tScale, color=bg, marker='.')
# Styling
ax.set_aspect(aspect/ax.get_data_ratio())
###############################################################################
# Debugging
###############################################################################
minT = min(df['Time'])
df[df['Time']==minT]