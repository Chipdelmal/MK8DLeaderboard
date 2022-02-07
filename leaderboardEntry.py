
import sys
import time
import pandas as pd
import constants as const
from os import path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


(TRK, SPD, ITM) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (TRK, SPD, ITM) = ('Bonus', '200cc', 'NoItems')
BASE_URL = 'https://www.speedrun.com'
(DRV, OUT) = (
    '/home/chipdelmal/Documents/GitHub/MK8DLeaderboard/chromedriver/chromedriver',
    '/home/chipdelmal/Documents/MK8D/Leaderboard/'
)
df = pd.read_csv(
    path.join(OUT, 'LeadHistory-{}_{}-{}.csv'.format(TRK, SPD, ITM)), 
    names=['Link']
)
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
i = 30
entriesList = []
for i in range(0, entriesNum):
    entry = df.iloc[i]['Link']
    # Get page
    driver.get(entry)
    # Get sumbision dates
    (submT, dateT) = (
        driver.find_element_by_xpath(submX).text,
        driver.find_element_by_xpath(dateX).text
    )
    # Get submission time
    head = driver.find_element_by_xpath(runtX).text
    headSplit = head.split('-')
    (cat, time) = (headSplit[0], headSplit[1])
    if len(headSplit) > 3:
        pString = [i.strip() for i in time.split('in')[1].split('by')]
        (runtT, authT) = (pString[0], pString[1])
        authT = authT.replace(" (Obsolete)\nIn", "")
    elif len(headSplit) == 3:
        pString = [i.strip() for i in time.split('in')[1].split('by')]
        (runtT, authT) = (pString[0], pString[1])
        authT = authT.replace(" (Obsolete)\nIn", "")
    else:
        pString = [i.strip() for i in time.split('\n')[0].split('in')[1].split('by')]
        (runtT, authT) = (pString[0], pString[1])
        authT = authT.replace(" (Obsolete)", "")
    authT = authT.split('(Obsolete)')[0].strip()
    # Assemble result
    row = (str(authT), runtT, dateT, submT)
    entriesList.append(row)
    # print('\t{}: {}'.format(str(i+1).zfill(3), row))
driver.quit()
###############################################################################
# Create and export dataframes
###############################################################################
cols = ['Runner', 'Time', 'Date', 'Submitted']
runsDF = pd.DataFrame(entriesList, columns=cols)
runsDF.to_csv(
    path.join(OUT, 'LeadEntries-{}_{}-{}.csv'.format(TRK, SPD, ITM)), 
    index=False
)