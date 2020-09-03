
import itertools
from subprocess import Popen, PIPE

# #############################################################################
# Define categories to download
# #############################################################################
(CAT, SPD, ITM) = (
        ('48', '32', 'Nitro', 'Retro', 'Bonus'),
        ('200cc', '150cc'), ('Items', 'NoItems')
    )
combs = list(itertools.product(*[CAT, SPD, ITM]))
# #############################################################################
# Parse the leaderboards to CSV files
# #############################################################################
msg = '* Scraping ({}/{}): {}          '
for (i, cSet) in enumerate(combs):
    print(msg.format(i+1, len(combs), cSet), end='\r')
    cmd = ['python3', 'scrape.py', cSet[0], cSet[1], cSet[2]]
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    process.wait()
