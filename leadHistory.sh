#!/bin/bash

echo "* Parsing runs links..."
python leaderboardHistory.py '48' '200cc' 'NoItems'
echo "* Parsing runs info..."
python leaderboardEntry.py '48' '200cc' 'NoItems'
echo "* Plotting runs..."
python leaderboardPlots.py '48' '200cc' 'NoItems'