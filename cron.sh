#!/bin/bash
if [ $(date "+%Y") != 2021 ]; then
    exit
fi

cd ~/MalodyChartJam/
mkdir -p log

dt="$(date '+%Y%d%m-%H%M%S')"
echo "Starting on $dt" >> recent_cron.log
sh fetch_and_update.sh $1 > "log/$dt.log" 2> "log/$dt-err.log"
echo "Finished on $(date '+%Y%d%m-%H%M%S')" >> recent_cron.log
