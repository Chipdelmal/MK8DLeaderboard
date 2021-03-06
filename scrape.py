
import sys
import time
import dateparser
import pandas as pd
import functions as fun
import constants as const
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


(TRK, SPD, ITM) = (sys.argv[1], sys.argv[2], sys.argv[3])
(DRV, OUT) = (
    '/home/chipdelmal/Documents/GitHub/MK8DLeaderboard/chromedriver/chromedriver',
    '/home/chipdelmal/Documents/MK8D/Leaderboard/'
)
# (TRK, SPD, ITM) = ('48', '200cc', 'NoItems')
# Load driver and mainpage ----------------------------------------------------
print('* Loading selenium scraper...')
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(DRV, options=chrome_options)
driver.get(const.mainpage)
# Setup dictionaries for buttons ----------------------------------------------
print('* Selecting leaderboard...')
catDict = const.catSelector(TRK)
(trkBtn, spdBtn, itmBtn) = (
    driver.find_elements_by_xpath(catDict.get('trk'))[0],
    driver.find_elements_by_xpath(catDict.get('spd').get(SPD))[0],
    driver.find_elements_by_xpath(catDict.get('itm').get(ITM))[0]
)
trkBtn.click()
itmBtn.click()
spdBtn.click()
time.sleep(3)
# Get table -------------------------------------------------------------------
print('* Parsing leaderboard table...')
table = driver.find_elements_by_tag_name('table')[0]
rowNum = len(table.find_elements_by_tag_name('tr'))
# Iterate through table rows --------------------------------------------------
ldBrd = pd.DataFrame(columns=('Rank', 'Player', 'Time', 'Version', 'Date'))
(rix, rank) = (0, 1)
for (rix, rank) in enumerate(range(1, rowNum)):
    rowIx = rank + 1
    # Load Row ----------------------------------------------------------------
    tblRowStr = const.tblRow.format(rowIx) + '/td[{}]'
    tblRowXPth = [tblRowStr.format(i) for i in range(1, 9)]
    (rnk, nam, tme, ver, dte) = fun.getRow(driver, tblRowXPth)
    # Time --------------------------------------------------------------------
    tS = fun.parseTimeString(tme)
    tR = (tS.seconds + tS.microseconds * 1E-6) / 60
    # Date --------------------------------------------------------------------
    dteS = dateparser.parse(dte)
    # Rank --------------------------------------------------------------------
    rnkS = fun.stripRank(rnk)
    # Add row to dataframe ----------------------------------------------------
    ldBrd = ldBrd.append(
        {
            'Rank': rnkS, 'Player': nam, 'Time': tR,
            'Version': ver, 'Date': dteS
        },
        ignore_index=True
    )
# ldBrd = ldBrd.set_index('Rank')
# Export CSV ------------------------------------------------------------------
todayStamp = str(dateparser.parse('now'))[:10]
print('* Exporting CSV...')
ldBrd.to_csv('{}{}_{}_{}_{}.csv'.format(OUT, todayStamp, TRK, SPD, ITM))
# Done ------------------------------------------------------------------------
driver.quit()
print('* Done!')

# tblRowXPth = [tblRowStr.format(i) for i in range(1, 9)]
# [driver.find_elements_by_xpath(el)[0].text for el in tblRowXPth]
# tst = driver.find_elements_by_xpath('//*[@id="primary-leaderboard"]/tbody/tr[2]/td[6]')
# //*[@id="primary-leaderboard"]/tbody/tr[9]/td[6]

