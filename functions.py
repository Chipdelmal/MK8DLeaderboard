
import re
from datetime import timedelta
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap


regex = re.compile(
        r'((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?((?P<milliseconds>\d+?)ms)?'
    )


def parseTimeString(timeStr):
    clnTime = timeStr.replace(' ', '')
    parts = regex.match(clnTime)
    parts = parts.groupdict()
    time_params = {}
    for name in parts.keys():
        if parts[name] is not None:
            time_params[name] = int(parts[name])
    time_params
    return timedelta(**time_params)


def parseTime(ts):
    return [int(re.sub("[^0-9]", "", t)) for t in ts]


def getTiming(time):
    ts = time.split()
    if len(ts) == 4:
        (h, m, s, ms) = parseTime(ts)
        td = timedelta(hours=h, minutes=m, seconds=s, milliseconds=ms)
    elif len(ts) == 3:
        (h, m, s) = parseTime(ts)
        td = timedelta(hours=h, minutes=m, seconds=s)
    else:
        (m, s) = parseTime(ts)
        td = timedelta(hours=0, minutes=m, seconds=s)
    return td


def getRow(driver, tblRowXPth):
    (place, name, time) = (
        driver.find_elements_by_xpath(el)[0].text for el in tblRowXPth[0:3]
    )
    (version, date) = (
            driver.find_elements_by_xpath(el)[0].get_attribute('textContent') 
            for el in tblRowXPth[5:7]
    )
    # Fix for leaderboards without "real-time" column
    if (len(version)==0) or (len(date)==0):
        (version, date) = (
                driver.find_elements_by_xpath(el)[0].get_attribute('textContent') 
                for el in tblRowXPth[4:6]
        )
    return (place, name, time, version, date)


def stripRank(rankStr):
    cln = rankStr.replace('th', '').replace('st', '')
    cln = cln.replace('nd', '').replace('rd', '')
    return cln


def getPlayerRanks(name, boards):
    (ranks, times) = ([], [])
    for brd  in boards:
        row = brd[brd['Player']==name]
        if (row.shape[0]>0):
            (rank, time) = (
                row['Rank'].values[0], 
                row['Time'].values[0]
            )
        else:
            (rank, time) = (np.nan, np.nan)
        ranks.append(rank)
        times.append(time)
    return (ranks, times)


def colorPaletteFromHexList(clist):
    c = mcolors.ColorConverter().to_rgb
    clrs = [c(i) for i in clist]
    rvb = mcolors.LinearSegmentedColormap.from_list("", clrs)
    return rvb


def titleSelector(TRK, SPD, ITM):
    (track, speed, items) = ('', '', '')
    # Tracks
    if TRK == '48':
        track = '48 Tracks'
    elif TRK == '32':
        track = '32 Tracks'
    elif TRK == 'Nitro':
        track = 'Nitro Tracks'
    else:
        track = 'Retro Tracks'
    # Speeds
    speed = SPD
    # Items
    if ITM == 'NoItems':
        items = 'No Items'
    else:
        items = 'Items'
    # Return
    return '{}, {}, {}'.format(track, speed, items)