#!/bin/bash
ISAWAKE=$(ps aux | grep bot | head -n1 | grep py -c)
if [ $ISAWAKE -ne 1 ]
then
    screen -X -S botnc quit
    screen -S botnc -d -m /usr/bin/python /home/betezed/botnc/main.py
    date +"%y-%m-%d %T Restart" >> /home/betezed/botnc/log.txt
else
    ps aux | grep bot | head -n1 | awk -F " " '{print $2}'
    echo "Allumé"
fi
