#!/bin/bash
# Replace these two settings.

##############

CUR_PATH=$(cd "$(dirname "$0")"; pwd)

PID_FILE=wms.uudragon.pid

PYTHON_DIR=/usr/local/python2.7/bin

SOURCE_DIR=/export/Apps/wms.uudragon.com

####

HOST=0.0.0.0

PORT=9099

##############

$PYTHON_DIR/python $SOURCE_DIR/manage.py runfcgi method=threaded host=$HOST port=$PORT pidfile=$CUR_PATH/$PID_FILE errlog=$CUR_PATH/../logs/error.log outlog=$CUR_PATH/../logs/out.log &
