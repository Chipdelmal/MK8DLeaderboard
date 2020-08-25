
import sys
import time
import dateparser
import pandas as pd
import functions as fun
import constants as const
from selenium import webdriver


(SPD, ITM) = (sys.argv[1], sys.argv[2])
(DRV, OUT) = ('./chromedriver/chromedriver_macos', './out/')
# (SPD, ITM) = ('200cc', 'NoItems')
# Load driver and mainpage ----------------------------------------------------
print('* Loading selenium scraper...')
driver = webdriver.Chrome(DRV)
driver.get(const.mainpage)
# Setup dictionaries for buttons ----------------------------------------------
print('* Selecting leaderboard...')
(catBtn, spdBtn) = (
        driver.find_elements_by_xpath(const.catSpeed.get(SPD))[0],
        driver.find_elements_by_xpath(const.catItems.get(ITM))[0]
    )
catBtn.click()
spdBtn.click()
time.sleep(5)
# Get table -------------------------------------------------------------------
print('* Parsing leaderboard table...')
table = driver.find_elements_by_tag_name('table')[0]
rowNum = len(table.find_elements_by_tag_name('tr'))
# Iterate through table rows --------------------------------------------------
ldBrd = pd.DataFrame(columns=('Rank', 'Player', 'Time', 'Version', 'Date'))
for (rix, rank) in enumerate(range(1, rowNum)):
    rowIx = rank + 1
    # Load Row ----------------------------------------------------------------
    tblRowStr = const.tblRow.format(rowIx)+'/td[{}]'
    tblRowXPth = [tblRowStr.format(i) for i in range(1, 7)]
    (rnk, nam, tme, ver, dte) = fun.getRow(driver, tblRowXPth)
    # Time --------------------------------------------------------------------
    tS = fun.getTiming(tme)
    tR = (tS.seconds + tS.microseconds * 1E-6) / 60
    # Date --------------------------------------------------------------------
    dteS = dateparser.parse(dte)
    # Rank --------------------------------------------------------------------
    rnkS = fun.stripRank(rnk)
    # Add row to dataframe ----------------------------------------------------
    ldBrd = ldBrd.append({
                'Rank': rnkS, 'Player': nam, 'Time': tR,
                'Version': ver, 'Date': dteS
            }, ignore_index=True
        )
ldBrd = ldBrd.set_index('Rank')
# Export CSV ------------------------------------------------------------------
print('* Exporting CSV...')
ldBrd.to_csv('{}{}-{}.csv'.format(OUT, SPD, ITM))
# Done ------------------------------------------------------------------------
print('* Done!')
