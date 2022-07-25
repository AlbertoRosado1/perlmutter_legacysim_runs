#!/bin/bash
# EXAMPLE bash split_bricklist.sh south 2000
run=$1 # north or south
number_of_bricks=$2 # 1000
split -d -l $number_of_bricks bricklist_"$run".txt splitted_bricklists/bricklist_"$run"_
#--numeric-suffixes --suffix-length=3