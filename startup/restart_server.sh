#!/bin/bash

# Replace these three settings.
PROJDIR=`pwd`
PIDFILE="${PROJDIR}/mysite.pid"
SOCKET="${PROJDIR}/mysite.sock"

echo $PIDFILE

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

python ./manage.py runfcgi host=127.0.0.1 port=8080 pidfile=$PIDFILE
