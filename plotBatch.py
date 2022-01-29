
import os
from subprocess import Popen, PIPE


fldr = '/home/chipdelmal/Documents/MK8D/Leaderboard'
flst = [each for each in os.listdir(fldr) if each.endswith('.csv')]
# #############################################################################
# Parse the leaderboards to CSV files
# #############################################################################
msg = '* Plotting ({}/{}): {}          '
for (i, fName) in enumerate(flst):
    print(msg.format(i+1, len(flst), fName), end='\r')
    cmd = ['python', 'plot.py', fName]
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    process.wait()
