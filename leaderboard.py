
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
###############################################################################
# Load driver and mainpage
###############################################################################
print('* Loading selenium scraper...')
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(DRV, options=chrome_options)
driver.get(const.mainpage)
a = ActionChains(driver)
###############################################################################
# Setup dictionaries for buttons
###############################################################################
print('* Selecting leaderboard...')
catDict = const.catSelector(TRK)
(trkBtn, spdBtn, itmBtn) = (
    driver.find_elements_by_xpath(catDict.get('trk'))[0],
    driver.find_elements_by_xpath(catDict.get('spd').get(SPD))[0],
    driver.find_elements_by_xpath(catDict.get('itm').get(ITM))[0]
)
trkBtn.click(); itmBtn.click(); spdBtn.click()
time.sleep(3)
###############################################################################
# Open obsolete runs
###############################################################################
fltr = '//*[@id="leaderboard-menu"]/div/div[2]/div[1]/button'
fltrBtn = driver.find_element_by_xpath(fltr)
fltrBtn.click()
# Hover on obsolete runs
obs = '//*[@id="leaderboard-menu"]/div/div[2]/div[1]/ul/li[4]/a'
obsBtn = driver.find_element_by_xpath(obs)
a.move_to_element(obsBtn).perform()
# Highlight show obsolete
shwn = '//*[@id="leaderboard-menu"]/div/div[2]/div[1]/ul/li[4]/ul/a[2]'
shwnBtn = driver.find_elements_by_xpath(shwn)[0]
shwnBtn.click()
###############################################################################
# Get table rows (links to runs)
###############################################################################
xPath = '//*[@id="primary-leaderboard"]/tbody/tr[{}]'
rows = 604 # len(driver.find_elements_by_tag_name('tr'))
runLinks = []
for row in range(1, rows):
    r = xPath.format(row)
    rObj = driver.find_element_by_xpath(r)
    runLink = rObj.get_attribute('data-target')
    runLinks.append(BASE_URL+runLink)
###############################################################################
# Export list to file
###############################################################################
runLinksDF = pd.DataFrame(runLinks, columns=['Link'])
runLinksDF.to_csv(path.join(OUT, 'leadHistory.csv'), index=False, header=False)