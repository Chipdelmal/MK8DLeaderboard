

mainpage = 'https://www.speedrun.com/mk8dx'
catTrack = {
        '48': '//*[@id="category73495"]',
        '32': '//*[@id="category73494"]',
        'Nitro': '//*[@id="category47231"]',
        'Retro': '//*[@id="category47232"]',
        'Bonus': '//*[@id="category47233"]'
    }
catItems = {
        'Items': '//*[@id="varnav23164"]/label[1]',
        'NoItems': '//*[@id="varnav23164"]/label[2]'
    }
catSpeed = {
        '150cc': '//*[@id="varnav11257"]/label[1]',
        '200cc': '//*[@id="varnav11257"]/label[2]'
    }
tblRow = '//*[@id="leaderboarddiv"]/table/tbody/tr[{}]'

# #############################################################################
# Categories XPath Dictionaries
# #############################################################################
tracks48 = {
        'trk': '//*[@id="category73495"]',
        'itm': {
                'Items': '//*[@id="varnav23164"]/label[1]',
                'NoItems': '//*[@id="varnav23164"]/label[2]'
            },
        'spd': {
                '150cc': '//*[@id="varnav11257"]/label[1]',
                '200cc': '//*[@id="varnav11257"]/label[2]'
            }
    }

tracks32 = {
        'trk': '//*[@id="category73494"]',
        'itm': {
                'Items': '//*[@id="varnav23162"]/label[1]',
                'NoItems': '//*[@id="varnav23162"]/label[2]'
            },
        'spd': {
                '150cc': '//*[@id="varnav11257"]/label[1]',
                '200cc': '//*[@id="varnav11257"]/label[2]'
            }
    }

tracksNitro = {
        'trk': '//*[@id="category47231"]',
        'itm': {
                'Items': '//*[@id="varnav11254"]/label[1]',
                'NoItems': '//*[@id="varnav11254"]/label[2]'
            },
        'spd': {
                '150cc': '//*[@id="varnav11257"]/label[1]',
                '200cc': '//*[@id="varnav11257"]/label[2]'
            }
    }

tracksRetro = {
        'trk': '//*[@id="category47232"]',
        'itm': {
                'Items': '//*[@id="varnav11255"]/label[1]',
                'NoItems': '//*[@id="varnav11255"]/label[2]'
            },
        'spd': {
                '150cc': '//*[@id="varnav11257"]/label[1]',
                '200cc': '//*[@id="varnav11257"]/label[2]'
            }
    }

tracksBonus = {
        'trk': '//*[@id="category47233"]',
        'itm': {
                'Items': '//*[@id="varnav11256"]/label[1]',
                'NoItems': '//*[@id="varnav11256"]/label[2]'
            },
        'spd': {
                '150cc': '//*[@id="varnav11257"]/label[1]',
                '200cc': '//*[@id="varnav11257"]/label[2]'
            }
    }


def catSelector(cat):
    if (cat == '48'):
        return tracks48
    if (cat == '32'):
        return tracks32
    if (cat == 'Nitro'):
        return tracksNitro
    if (cat == 'Retro'):
        return tracksRetro
    if (cat == 'Bonus'):
        return tracksBonus
