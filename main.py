
import time
import numpy as np
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
ran = 175
times = [None] * ran
(timesC, timesD) = ([], [])
for (rix, rank) in enumerate(range(1, ran+1)):
    # rank = 44
    # Preprocess table
    rowIx = rank + 1
    # row = table.find_elements_by_xpath(const.tblRow.format(rowIx))[0]
    tblRowStr = const.tblRow.format(rowIx)+'/td[{}]'
    tblRowXPth = [tblRowStr.format(i) for i in range(1, 7)]
    (place, name, time, version, date) = fun.getRow(driver, tblRowXPth)
    # row.text
    tS = fun.getTiming(time)
    ttS = (tS.seconds + tS.microseconds * 1E-6) / 60
    times[rix] = ttS
    if version == 'Digital':
        timesD.append(ttS)
    else:
        timesC.append(ttS)
# Plotting
bins = 20
# sns.distplot(times, bins=50, rug=True, hist=True, kde=False, color="#812184")
sns.distplot(timesD, bins=bins, rug=True, hist=True, kde=False, label='Digital', color="#1344b8")
sns.distplot(timesC, bins=bins, rug=True, hist=True, kde=False, label='Cartridge', color="#ed174b")
timesSlices = [times[i] for i in np.arange(0, 150, 10)]
[plt.axvline(i, lw=.15) for i in timesSlices]
plt.legend(prop={'size': 12})
plt.title('Leaderboard Frequency Histograms')
plt.xlabel('Time (minutes)')
plt.ylabel('Frequency')



fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(2, 4), sharey=True)
ax.set_title('Default violin plot')
ax.set_ylabel('Observed values')
ax.violinplot(
        [timesD, timesC, times],
        showmeans=False, showmedians=False, showextrema=False
    )
