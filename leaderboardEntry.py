
import sys
import csv
import time
import pandas as pd
import constants as const
from os import path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


# (TRK, SPD, ITM) = (sys.argv[1], sys.argv[2], sys.argv[3])
BASE_URL = 'https://www.speedrun.com'
(DRV, OUT) = (
    '/home/chipdelmal/Documents/GitHub/MK8DLeaderboard/chromedriver/chromedriver',
    '/home/chipdelmal/Documents/MK8D/Leaderboard/'
)
(TRK, SPD, ITM) = ('48', '200cc', 'NoItems')
print('* Parsing entries...')
df = pd.read_csv(path.join(OUT, 'leadHistory.csv'), names=['Link'])
entriesNum = df.shape[0]
###############################################################################
# Load driver and mainpage
###############################################################################
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(DRV, options=chrome_options)
driver.get(const.mainpage)
a = ActionChains(driver)
###############################################################################
# Load driver and mainpage
###############################################################################
(submX, dateX, runtX) = (
    '//*[@id="centerwidget"]/div[2]/div[2]/div/div[1]/time',
    '//*[@id="centerwidget"]/div[2]/div[2]/div/div[2]/time',
    '//*[@id="centerwidget"]/div[2]/div[1]'
)
# Iterate through entries
i = 4
entriesList = []
for i in range(entriesNum):
    entry = df.iloc[i]['Link']
    # Get page
    driver.get(entry)
    # Get sumbision dates
    (submT, dateT) = (
        driver.find_element_by_xpath(submX).text,
        driver.find_element_by_xpath(dateX).text
    )
    # Get submission time
    head = driver.find_element_by_xpath(t).text
    headSplit = head.split('-')
    if len(headSplit) > 3:
        (cat, time, _, _ ) = headSplit
        (runtT, authT) = [i.strip() for i in time.split('in')[1].split('by')]
        authT = authT.replace(" (Obsolete)\nIn", "")
    elif len(headSplit) == 3:
        (cat, time, _) = headSplit
        (runtT, authT) = [i.strip() for i in time.split('in')[1].split('by')]
        authT = authT.replace(" (Obsolete)\nIn", "")
    else:
        (cat, time) = headSplit
        (runtT, authT) = [i.strip() for i in time.split('\n')[0].split('in')[1].split('by')]
        authT = authT.replace(" (Obsolete)", "")
    # Assemble result
    row = (authT, runtT, dateT, submT)
    entriesList.append(row)
    print(row)
###############################################################################
# Create and export dataframes
###############################################################################
runsDF = pd.DataFrame(
    entriesList, columns=['Runner', 'Time', 'Date', 'Submitted in']
)
runsDF.to_csv(path.join(OUT, 'leadRunsHistory.csv'))