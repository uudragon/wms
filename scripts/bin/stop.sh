#!/bin/bash

##############

CUR_PATH=$(cd "$(dirname "$0")"; pwd)

PIDFILE=$CUR_PATH/wms.uudragon.pid

##############

if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi
