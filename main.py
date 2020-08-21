
import re
from datetime import timedelta
from selenium import webdriver
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys


(DRV, OUT) = ('./chromedriver/chromedriver', './out/')
(SPD, ITM) = ('200cc', 'NoItems')
# Load driver and mainpage ----------------------------------------------------
driver = webdriver.Chrome(DRV)
driver.get('https://www.speedrun.com/mk8dx')
# Setup dictionaries for buttons ----------------------------------------------
catItems = {
        'Items': '//*[@id="varnav23164"]/label[1]',
        'NoItems': '//*[@id="varnav23164"]/label[2]'
    }
catSpeed = {
        '150cc': '//*[@id="varnav11257"]/label[1]',
        '200cc': '//*[@id="varnav11257"]/label[2]'
    }
tblRow = '//*[@id="leaderboarddiv"]/table/tbody/tr[{}]'
# Click the category and items buttons
(catBtn, spdBtn) = (
        driver.find_elements_by_xpath(catSpeed.get(SPD))[0],
        driver.find_elements_by_xpath(catItems.get(ITM))[0]
    )
catBtn.click()
spdBtn.click()
# Get table -------------------------------------------------------------------
table = driver.find_elements_by_tag_name('table')[0]

# Iterate through table rows --------------------------------------------------
rowIx = 2

row = table.find_elements_by_xpath(tblRow.format(rowIx))[0]
entryXPth = [tblRow.format(rowIx)+'/td[{}]'.format(i) for i in range(1, 6)]
(place, name, time, version, date) = (
        driver.find_elements_by_xpath(el)[0].text for el in entryXPth
    )
# row.text
(h, m, s, ms) = [int(re.sub("[^0-9]", "", t)) for t in time.split()]
str(timedelta(hours=h, minutes=m, seconds=s, milliseconds=ms))
