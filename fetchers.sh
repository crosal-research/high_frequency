#!/bin/bash
############################################################
# Author: Joã Mauricio Rosal
# Last change: 09/92/2021
# This script:
# 1) fetches daily data for covid, energy consumption, 
#    mobility from apple iphone signals and vaccines
# 2) inserts these data into a sqlite database (DB)
# 3) Starts a local servers that accepts requests on this DB
# 4) Generate charts from the data in the DB
# 5) Shuts down the servers
############################################################


# python scripts to fetch data and insert in the DB
python3 -m DB.Fetchers.covid_international 
python3 -m DB.Fetchers.ons 
python3 -m DB.Fetchers.mobility_apple 
python3 -m DB.Fetchers.owid
python3 -m DB.Fetchers.energia_fetch_all

echo "Done fetching data!"
echo -e "----------\n"


# python scritp to ignite local server @ localhost:8080
python3 -m DB.API.user_api &

# checks whether the server is already runing
process= 

while [ -z "$process" ]; do
    sleep 1.0
    process=$(lsof -i -P | grep -i "localhost:8080" | awk '{print $2}')
done;

echo "Server is running with pid $process"
echo -e "--------\n"

# Remove old charts
rm ./images/*

echo "Old exhibits cleaned up!"
echo -e "-------\n"

# python scripts to generate charts
./charts/chart_covid.py
./charts/chart_mobility.py
./charts/chart_vaccines.py 
./charts/chart_ons.py 

# kills server
kill $process
echo "Server killed"
echo "----------"

