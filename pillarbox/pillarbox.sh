#! /bin/sh
# Copyright (c) 2014 Kelcey Damage
# All rights reserved.
#
# Author: Kelcey Damage, 2016
#
# /etc/init.d/pillarbox
#   and its symbolic link
# $PROG_PATH/pillarbox.sh

### BEGIN INIT INFO
# Provides:          Pillar Box
# Required-Start:
# Required-Stop:
# Default-Start:     3 5
# Default-Stop:      0 1 2 6
# Short-Description: pillarbox is providing a routing endpoint for Sherpa
# Description:       pillarbox is a minor socket server that receives
# 					         routing requests from Sherpa, and forwards objects
#                    to a storage backend. pillarbox can also act as a
#                    file-backed backend.
#	service.  We want it to be active in runlevels 3
#	and 5, as these are the runlevels with the network
#	available.
### END INIT INFO

## Fill in name of program here.
PROG="pillarbox"
PROG_PATH="/opt/sherpa/pillarbox/" ## Not need, but sometimes helpful (if $PROG resides in /opt for example).
PID_PATH="/var/run"
PROG_ARGS=""

start() {
    if [ -e "$PID_PATH/$PROG.pid" ]; then
        ## Program is running, exit with error.
        echo "Error! $PROG is currently running!" 1>&2
        exit 1
    else
        ## Change from /dev/null to something like /var/log/$PROG if you want to save output.
            $PROG_PATH/$PROG $PROG_ARGS 1>&2 &
        echo "$PROG started"
        touch "$PID_PATH/$PROG.pid"
    fi
}

stop() {
    if [ -e "$PID_PATH/$PROG.pid" ]; then
        ## Program is running, so stop it
        kill -9 $(cat $PID_PATH/$PROG.pid)

        rm -rf "$PID_PATH/$PROG.pid"

        echo "$PROG stopped"
    else
        ## Program is not running, exit with error.
        echo "Error! $PROG not started!" 1>&2
        exit 1
    fi
}

status() {
    if [ -e "$PID_PATH/$PROG.pid" ]; then
        echo "Pillar Box is running (pid $(cat $PID_PATH/$PROG.pid))"
    else
        echo "Pillar Box is not running"
    fi
}

## Check to see if we are running as root first.
## Found at http://www.cyberciti.biz/tips/shell-root-user-check-script.html
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

case "$1" in
    start)
        start
        exit 0
    ;;
    stop)
        stop
        exit 0
    ;;
    status)
        status
        exit 0
    ;;
    reload|restart|force-reload)
        stop
        start
        exit 0
    ;;
    **)
        echo "Usage: $0 {start|stop|reload}" 1>&2
        exit 1
    ;;
esac
rc_exit
