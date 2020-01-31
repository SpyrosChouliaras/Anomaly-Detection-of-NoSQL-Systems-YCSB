#!/bin/bash
PATH=/usr/local/maven/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin

cd /home/spyros/YCSB

echo " ------------------------------------------------------------"

echo "                    load the workload                        "

echo " ------------------------------------------------------------"


./bin/ycsb load mongodb -s -P workloads/workloadb > outputLoad.txt


echo " ------------------------------------------------------------"

echo "                    Run The Workload                         "

echo " ------------------------------------------------------------"


./bin/ycsb run mongodb -s -P workloads/workloadb > outputRun.txt



mongo ycsb --eval "print(db.dropDatabase())"
