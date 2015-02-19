#!/bin/bash


#  pg_restore -c -i -U cspace -d "cspace" -v /tmp/backup.sql
#  pg_restore -c -i -U nuxeo -d "nuxeo" -v /tmp/backupNuxeo.sql
#  pg_dump -h 'cs-sql-01' -U cspace cspace -F t -f backupcspace.sql
#  pg_dump -h 'cs-sql-01' -U nuxeo nuxeo -F t -f backupnuxeo.sql


host="cs-sql-01"
dayname="$(date +'%a')"
daycounter="$(date +'%u')"
hourcounter="$(date +'%H')"
weekcounter="$(date +'%W')"
monthcounter="$(date +'%b')"
yearcounter="$(date +'%Y')"
log="/home/thw/log/pg_bu.txt"
cspacedumpfile="/home/thw/backup/backup_${host}_cspace_${daycounter}${hourcounter}.sql"
nuxeodumpfile="/home/thw/backup/backup_${host}_nuxeo_${daycounter}${hourcounter}.sql"
weeknuxeodumpfile="/home/thw/backup/backup_${host}_nuxeo_${weekcounter}-${monthcounter}-${yearcounter}.sql"
doRestore=0

source /home/thw/bashrc
unixstart=`perl -e 'print int(time)'`
echo "------ `date` -----" >> $log

# do cspace
echo "DUMPSTART $unixstart" >> $log
echo "did dump to $cspacedumpfile" >> $log


pg_dump -h $host -U cspace cspace -F t -f $cspacedumpfile >> $log 2>&1
dumpstatus=$?
echo "$dumpstatus" >> $log

if [ $dumpstatus -eq 0 ]; then
        echo "do pg_restore -c -i -U cspace -d 'cspace' -v $cspacedumpfile" >> $log
        if [ $doRestore -eq 1 ]; then
                pg_restore -c -i -U cspace -d "cspace" -v $cspacedumpfile >> $log 2>&1
                restorestatus=$?
                echo "$restorestatus" >> $log
        else
                echo "no restore" >> $log
        fi
else
        echo "bad dumpstatus: $dumpstatus" >> $log
        #exit
fi

# do nuxeo
if [ "$dayname" == "man" -a ! -e "$weeknuxeodumpfile" ]; then
        pg_dump -h $host -U nuxeo nuxeo -F t -f $weeknuxeodumpfile >> $log 2>&1

else
        pg_dump -h $host -U nuxeo nuxeo -F t -f $nuxeodumpfile >> $log 2>&1
fi
dumpstatus=$?
echo "$dumpstatus" >> $log

if [ $dumpstatus -eq 0 ]; then
        echo "do pg_restore -c -i -U nuxeo -d 'nuxeo' -v $nuxeodumpfile" >> $log
        if [ $doRestore -eq 1 ]; then
                #pg_restore -c -i -U nuxeo -d "nuxeo" -v $nuxeodumpfile >> $log 2>&1
                restorestatus=$?
                echo "$restorestatus" >> $log
        else
                echo "no nuxeo restore" >> $log
        fi
else
        echo "bad dumpstatus: $dumpstatus" >> $log
        #exit

fi

unixstop=`perl -e 'print int(time)'`
echo "DUMPSTOP $unixstop" >> $log


