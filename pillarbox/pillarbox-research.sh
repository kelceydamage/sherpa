##!/usr/bin/env python
# Author: Kelcey Jamison-Damage
# Python: 2.66 +
# OS: CentOS | Other
# Portable: True
# License: Apache 2.0

# License
#-----------------------------------------------------------------------#
# Copyright [2016] [Kelcey Jamison-Damage]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#-----------------------------------------------------------------------#

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
PROG="pillarbox.py"
PROG_PATH="/opt/palantir/research/pillarbox" ## Not need, but sometimes helpful (if $PROG resides in /opt for example).
PID_PATH="var/run"
PROG_ARGS=""

start() {
    if [ -e "$PID_PATH/$PROG.pid" ]; then
        ## Program is running, exit with error.
        echo "Error! $PROG is currently running!" 1>&2
        exit 1
    else
        ## Change from /dev/null to something like /var/log/$PROG if you want to save output.
        $PROG_PATH/$PROG $PROG_ARGS 1>&2 &
        PID=$!	
	echo $PID > $PID_PATH/$PROG.pid
	echo "$PROG started"
    fi
}

stop() {
    if [ -e "$PID_PATH/$PROG.pid" ]; then
        ## Program is running, so stop it
	PID=`cat $PID_PATH/$PROG.pid`
        kill -9 $PID

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
