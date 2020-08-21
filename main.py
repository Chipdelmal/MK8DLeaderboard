
import time
import seaborn as sns
import functions as fun
import constants as const
from selenium import webdriver
import matplotlib.pyplot as plt
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys


(DRV, OUT) = ('./chromedriver/chromedriver', './out/')
(SPD, ITM) = ('200cc', 'NoItems')
# Load driver and mainpage ----------------------------------------------------
driver = webdriver.Chrome(DRV)
driver.get(const.mainpage)
# Setup dictionaries for buttons ----------------------------------------------

# Click the category and items buttons
(catBtn, spdBtn) = (
        driver.find_elements_by_xpath(const.catSpeed.get(SPD))[0],
        driver.find_elements_by_xpath(const.catItems.get(ITM))[0]
    )
catBtn.click()
spdBtn.click()
time.sleep(3)
# Get table -------------------------------------------------------------------
table = driver.find_elements_by_tag_name('table')[0]
# Iterate through table rows --------------------------------------------------
ran = 150
times = [None] * ran
for (rix, rank) in enumerate(range(1, ran+1)):
    # rank = 44
    # Preprocess table
    rowIx = rank + 1
    # row = table.find_elements_by_xpath(const.tblRow.format(rowIx))[0]
    tblRowStr = const.tblRow.format(rowIx)+'/td[{}]'
    tblRowXPth = [tblRowStr.format(i) for i in range(1, 6)]
    (place, name, time, version, date) = fun.getRow(driver, tblRowXPth)
    # row.text
    tS = fun.getTiming(time)
    ttS = tS.seconds + tS.microseconds * 1E-6
    times[rix] = ttS / 60
sns.kdeplot(times, color="blue", shade=True)
times
