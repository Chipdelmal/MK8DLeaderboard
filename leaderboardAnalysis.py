
import sys
import csv
import time
from os import path
import pandas as pd


BASE_URL = 'https://www.speedrun.com'
(DRV, OUT) = (
    '/home/chipdelmal/Documents/GitHub/MK8DLeaderboard/chromedriver/chromedriver',
    '/home/chipdelmal/Documents/MK8D/Leaderboard/'
)
FNAME = 'leadRunsHistory_test.csv'

df = pd.read_csv(path.join(OUT, FNAME))
###############################################################################
# Cleaning datetimes
###############################################################################
df['Date'] =  pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.date
df['Submitted in'] =  pd.to_datetime(df['Submitted in'], format='%Y-%m-%d').dt.date
df['Time'] = pd.to_timedelta(df['Time'])
###############################################################################
# Processing data
###############################################################################
len(df['Date'].unique())
df['Runner'].unique()

df[df['Runner']=='chipdelmal']