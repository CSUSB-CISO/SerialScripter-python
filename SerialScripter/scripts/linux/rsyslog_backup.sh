#!/bin/bash

# need to check file size of file and ensure it is no bigger than 20 mbs or larger depending.

# if it is then move the file to a new file name that includes a timestamp and restart rsyslog.service

# if not then break/end program

timestamp=$(date +%H:%M)

if [ $(command -v stat) ]; then
    
    file_size=$(stat -c %s /var/log/rsyslog/rsyslog.log) 
    
    if [ $file_size -ge 20000000 ]; then
        mv /var/log/rsyslog/rsyslog.log /var/log/rsyslog/rsyslog.log$timestamp
        systemctl restart rsyslog
    fi

elif [ $(command -v du) ]; then
    file_size=$(du -h /var/log/rsyslog/rsyslog.log | cut -f 1 | cut -c 1) 

    if [ $file_size -ge 20 ]; then
        mv /var/log/rsyslog/rsyslog.log /var/log/rsyslog/rsyslog.log$timestamp
        systemctl restart rsyslog
    fi   
fi
