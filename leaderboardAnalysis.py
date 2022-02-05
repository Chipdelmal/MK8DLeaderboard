
from os import path
import pandas as pd

(TRK, SPD, ITM) = ('Nitro', '200cc', 'NoItems')
OUT = '/home/chipdelmal/Documents/MK8D/Leaderboard/'
###############################################################################
# Read file
###############################################################################
df = pd.read_csv(
    path.join(OUT, 'LeadEntries-{}_{}-{}.csv'.format(TRK, SPD, ITM))
)
###############################################################################
# Cleaning columns
###############################################################################
df['Runner'] = [str(i) for i in df['Runner']]
df['Date'] =  pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.date
df['Submitted in'] =  pd.to_datetime(df['Submitted'], format='%Y-%m-%d').dt.date
df['Time'] = pd.to_timedelta(df['Time'])
###############################################################################
# Processing
###############################################################################
dfPiv = df.pivot_table(
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
dfRnk.to_csv(
    path.join(OUT, 'LeadRanks-{}_{}-{}.csv'.format(TRK, SPD, ITM)), 
    index=True
)