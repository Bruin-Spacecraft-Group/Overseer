#!/bin/bash
rm -f .lock
CURRENT=`date +%s`
TO_WAIT=$(($CURRENT + ($1*60)))
echo $TO_WAIT > .to_wait
