
import time
import dateparser
import seaborn as sns
import pandas as pd
import functions as fun
import constants as const
from datetime import date
from datetime import datetime
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
time.sleep(5)
# Get table -------------------------------------------------------------------
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
    ldBrd = ldBrd.append(
            {
                'Rank': rnkS, 'Player': nam, 'Time': tR,
                'Version': ver, 'Date': dteS
            }, ignore_index=True
        )
ldBrd = ldBrd.set_index('Rank')
# Post process dataframe ------------------------------------------------------
bins = round(rowNum / 2)
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)
ax2 = sns.violinplot(
        x="Time", y='Version', hue="Version",
        data=ldBrd, palette='seismic', split=True, ax=ax2,
        cut=0
        # scale="count", inner="stick"
    )
ax1 = sns.distplot(
        ldBrd[ldBrd['Version'] == 'Digital'].get('Time'),
        bins=bins, kde=False, color="b", ax=ax1
    )
ax3 = sns.distplot(
        ldBrd[ldBrd['Version'] == 'Cartridge'].get('Time'),
        bins=bins, kde=False, color="r", ax=ax3
    )
for p in ax3.patches:  # turn the histogram upside down
    p.set_height(-p.get_height())
ax1.set_ylim(0, 7.5)
ax3.set_ylim(-7.5, 0)
ax2.legend_.remove()

# Scatter
diffs = []
for dt in ldBrd['Date']:
    today = dateparser.parse('today')
    delta = today - dt
    days = delta.days
    diffs.append(days)

ax4 = plt.scatter(ldBrd['Time'], y=diffs, alpha=0.5)
plt.yscale('log')
