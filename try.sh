#!/bin/bash
CURRENT=`date +%s`
TO_WAIT=`cat .to_wait`
if [ ! -f ".lock" ] && [ $TO_WAIT -le $CURRENT ]
then
    touch .lock
    ~/gpio_write.sh 1 && sleep 120
    ~/gpio_write.sh 0 || rm .lock
    fi
