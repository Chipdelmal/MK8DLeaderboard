
from os import path
import pandas as pd


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
# Exporting
###############################################################################
dfRnk.to_csv(path.join(OUT, 'leadRunsRanks.csv'), index=True)