
from os import path
from glob import glob
import pandas as pd

(IN, FILE, OUT) = (
    '/home/chipdelmal/Documents/MK8D/Leaderboard/',
    '*_48_200cc_NoItems.csv',
    '/home/chipdelmal/Documents/MK8D/Leaderboard/img/'
)
fnames = sorted(glob(path.join(IN, FILE)))
###############################################################################
# Process
###############################################################################
ldBrds = [pd.read_csv(i) for i in fnames]
namesLst = [i['Player'].unique() for i in ldBrds]
names = list(set(x for lst in names for x in lst))

name = 'Pianist15'
ranks = []
for brd  in ldBrds:
    row = brd[brd['Player']==name]
    rank = row['Rank'].values[0]
    ranks.append(rank)
ranks