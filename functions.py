
import re
from datetime import timedelta


def parseTime(ts):
    return [int(re.sub("[^0-9]", "", t)) for t in ts]


def getTiming(time):
    ts = time.split()
    if len(ts) == 4:
        (h, m, s, ms) = parseTime(ts)
        td = timedelta(hours=h, minutes=m, seconds=s, milliseconds=ms)
    else:
        (h, m, s) = parseTime(ts)
        td = timedelta(hours=h, minutes=m, seconds=s)
    return td


def getRow(driver, tblRowXPth):
    (place, name, time, version, date) = (
            driver.find_elements_by_xpath(el)[0].text for el in tblRowXPth
        )
    return (place, name, time, version, date)
