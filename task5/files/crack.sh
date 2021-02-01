#!/usr/bin/bash

for logfile in Logs/*.log; do
    ./dec.sh $logfile
done
