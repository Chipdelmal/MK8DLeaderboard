#!/bin/bash

declare -a cats=("32" "Retro" "Bonus" "Nitro" "48")
for catg in ${cats[@]}; do
    printf "* [Processing MK8D $catg]\n"
    printf "\t Parsing runs links...\n"
    python leaderboardHistory.py $catg '200cc' 'NoItems'
    printf "\t Parsing runs entries...\n"
    python leaderboardEntry.py $catg '200cc' 'NoItems'
    printf "\t Plotting runs...\n"
    python leaderboardPlots.py $catg '200cc' 'NoItems'
done
