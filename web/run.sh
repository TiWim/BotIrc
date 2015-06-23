#!/bin/sh
url="http://localhost:5668/0x90r00t/votes/"
RESPONSE=$(curl -sL $url -w "%{http_code}" -o /dev/null)
if [ $RESPONSE -eq "200" ]
then
    echo $RESPONSE
else
    screen -X -S ircweb quit
    screen -S ircweb -d -m /usr/bin/python /home/betezed/botnc/web/server2.py
    date +"%y-%m-%d %T Restart" >> /home/betezed/botnc/web/log.txt
fi
