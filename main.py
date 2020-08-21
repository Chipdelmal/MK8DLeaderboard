
from selenium import webdriver
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys


(DRV, OUT) = ('./chromedriver/chromedriver', './out/')
(SPD, ITM) = ('200cc', 'NoItems')
# Load driver and mainpage
driver = webdriver.Chrome(DRV)
driver.get('https://www.speedrun.com/mk8dx')
# Setup dictionaries for buttons
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
# Get table
table = driver.find_elements_by_tag_name('table')[0]

rowIx = 2
row = table.find_elements_by_xpath(tblRow.format(rowIx))[0]
row.text
tst = tblRow.format(rowIx) + '/td[1]'
table.find_elements_by_xpath(tst)[0].text
