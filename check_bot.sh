#!/bin/bash
if [ $# -eq 0 ]
then
    ARG=0
else
    ARG=$1
fi
ISAWAKE=$(ps aux | grep botnc/main | head -n1 | grep py -c)
if [ $ISAWAKE -ne 1 ]
then
    if [ $ARG -eq 1 ]
    then
        echo "Eteint"
    else
        echo "Launching ..."
        screen -X -S botnc quit
        screen -L -S botnc -d -m /bin/bash /home/betezed/botnc/run.sh
        date +"%y-%m-%d %T Restart" >> /home/betezed/botnc/log.txt
        sleep 1
        AWAKE=$(ps aux | grep botnc/main | head -n1 | grep py -c)
        if [ $AWAKE -eq 1 ]
        then
            PROCESS=$(ps aux | grep botnc/main | head -n1 | awk -F " " '{print $2}')
            echo "Launched with PID $PROCESS"
            date +"Success !" >> /home/betezed/botnc/log.txt
        else
            echo "Failure."
            date +"Failure ..." >> /home/betezed/botnc/log.txt
        fi

    fi
else
    PROCESS=$(ps aux | grep bot | head -n1 | awk -F " " '{print $2}')
    if [ $ARG -ne 1 ]
    then
        echo $PROCESS
        echo "Allumé"
    else 
        kill $PROCESS
        echo "Process $PROCESS killed"
    fi
fi
