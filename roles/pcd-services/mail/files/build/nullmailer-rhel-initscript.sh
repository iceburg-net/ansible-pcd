#!/bin/bash
#
# nullmailer simple MTA
#
# chkconfig: - 85 15
# description: nullmailer centos init @iceburg_net
# processname: nullmailer-send

### BEGIN INIT INFO
# Provides:          smtpdaemon
# Required-Start: $local_fs $network
# Required-Stop: $local_fs $network
# Short-Description: 
# Description:       
### END INIT INFO


# Source function library.
. /etc/init.d/functions

NAME=nullmailer
USER=nullmail

DAEMON=/usr/sbin/nullmailer-send
DAEMON_RUN_NAME=nullmailer-send
DAEMON_OPTS=

RETVAL=0

start() {
        echo -n "Starting $NAME: "
        
        PIDS=`pidof $DAEMON_RUN_NAME`
        if [ -z "$PIDS" ]; then
           daemon --user $USER $DAEMON $DAEMON_OPTS >> /var/log/nullmailer/nullmailer.log 2>&1 &
           return $?
        else
          echo "$NAME is already running"
          RETVAL=1
        fi
        
        return $RETVAL
}

stop() {
        echo -n "Shutting down $NAME: "
        
        PIDS=`pidof $DAEMON_RUN_NAME`
        if [ -n "$PIDS" ]; then
          killall $DAEMON_RUN_NAME
          return $?
        else
          echo "$NAME is not running"
          RETVAL=1
        fi

        return $RETVAL         
}

status() {
        echo -n "status not supported "
        return 0
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage: $NAME {start|stop|status|restart}"
        exit 1
        ;;
esac

exit $RETVAL