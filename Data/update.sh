#!/bin/bash

# Please execute this script every day (recommand crontab)

GET_ID_NAME_FILE="./norm_csv/fruit.csv"
if [ ! -f "$GET_ID_NAME_FILE" ]
then
    echo "update fruit id"
    find -O3 /home -name 'get_id_name_csv.py' -exec python3 '{}' \; 
    echo "fruit id update finished"
    wait
fi

echo "update raw csv"
find -O3 /home -name 'get_raw_csv.py' -exec python3 '{}' \; 
echo "raw csv update finished"

wait

echo "update norm csv"
find -O3 /home -name 'get_norm_csv.py' -exec python3 '{}' \; 
echo "norm csv update finished"

wait

echo "load data from csv to db"
find -O3 /home -name 'auto_data2db.py' -exec python3 '{}' \; 
echo "data load finished"
