#!/bin/bash

echo "* Parsing runs links..."
python leaderboardHistory.py
echo "* Parsing runs info..."
python leaderboardEntry.py
echo "* Plotting runs..."
python leaderboardPlots.py