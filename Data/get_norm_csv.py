import datetime
import requests
from datetime import date
import os
import csv
import sys
import re

def load_name_id():
    with open('./norm_csv/fruit.csv', 'r') as csvf:
        data = csv.DictReader(csvf)
        name_id = {}

        for row in data:
            name_id[row['name']] = row['id']

    return name_id

def get_fruit_month_csv(name_id):
    with open('./raw_csv/MonthlyProcudeFruit.csv', 'r') as csvf:
        data = csv.DictReader(csvf)

        with open('./norm_csv/fruit_month.csv', 'a') as csvf2:
            writer = csv.writer(csvf2)
            id_month = set()

            for row in data:
                if name_id.get(row['fruit_name']) != None:
                    id_month.add(name_id[row['fruit_name']] + ',' + row['month'])
            
            for item in id_month:
                writer.writerow(item.split(','))

def get_monthly_history_price_csv(name_id):
    with open('./raw_csv/MonthlyTrade.csv', 'r') as csvf:
        data = csv.reader(csvf)

        with open('./norm_csv/monthly_history_price.csv', 'a') as csvf2:
            writer = csv.writer(csvf2)

            for row in data:
                if name_id.get(row[0]) != None:
                    for i in range(2, 2+12):
                        writer.writerow([name_id[row[0]], row[i], row[1], i-1])

def get_daily_history_price_csv(name_id):
    with open('./raw_csv/DailyTrade.csv', 'r') as csvf:
        data = csv.DictReader(csvf)

        with open('./norm_csv/daily_history_price.csv', 'a') as csvf2:
            writer = csv.writer(csvf2)
            
            m = {}

            for row in data:
                if m.get(name_id[row['fruit_name']] + ',' + row['date']) != None:
                    m[name_id[row['fruit_name']] + ',' + row['date']][0] += float(row['price'])
                    m[name_id[row['fruit_name']] + ',' + row['date']][1] += 1
                else:
                    m[name_id[row['fruit_name']] + ',' + row['date']] = [float(row['price']), 1]
                    
            for key in m:
                temp = key.split(',')
                writer.writerow([temp[0], m[key][0] / m[key][1], temp[1]])

def get_location_csv(name_id):
    with open('./raw_csv/YearlyProcudeFruit.csv', 'r') as csvf:
        data = csv.DictReader(csvf)

        with open('./norm_csv/location.csv', 'a') as csvf2:
            writer = csv.writer(csvf2)
            location_id = {}

            id = 1
            for row in data:
                if name_id.get(row['fruit_name']) != None and location_id.get(row['County']) == None:
                    location_id[row['County']] = id
                    id += 1

            for key in location_id:
                writer.writerow([location_id[key], key])

def get_market_csv(name_id):
    with open('./raw_csv/DailyTrade.csv', 'r') as csvf:
        data = csv.DictReader(csvf)

        with open('./norm_csv/market.csv', 'a') as csvf2:
            writer = csv.writer(csvf2)
            id_market = set()

            for row in data:
                if name_id.get(row['fruit_name']) != None and (row['market_id'] + ',' + row['market_name']) not in id_market:
                    id_market.add(row['market_id'] + ',' + row['market_name'])
            
            for item in id_market:
                writer.writerow(item.split(','))

def get_fruit_location_csv(name_id):
    with open('./raw_csv/YearlyProcudeFruit.csv', 'r') as csvf:
        data = csv.DictReader(csvf)

        with open('./norm_csv/fruit_location.csv', 'a') as csvf2:
            writer = csv.writer(csvf2)
            location_fruit = set()

            for row in data:
                if name_id.get(row['fruit_name']) != None and (name_id[row['fruit_name']] + ',' + row['County']) not in location_fruit:
                    location_fruit.add(name_id[row['fruit_name']] + ',' + row['County'])
            
            for item in location_fruit:
                writer.writerow(item.split(','))

def init():
    if not os.path.isdir('./norm_csv'):
        os.mkdir("./norm_csv")
    
    with open('./norm_csv/fruit_month.csv', 'w') as csvf2:
        writer = csv.writer(csvf2)
        writer.writerow(['fruit_id', 'month'])

    with open('./norm_csv/monthly_history_price.csv', 'w') as csvf2:
        writer = csv.writer(csvf2)
        writer.writerow(['fruit_id', 'price', 'year', 'month'])
    
    with open('./norm_csv/daily_history_price.csv', 'w') as csvf2:
        writer = csv.writer(csvf2)
        writer.writerow(['fruit_id', 'price', 'date'])

    with open('./norm_csv/location.csv', 'w') as csvf2:
        writer = csv.writer(csvf2)
        writer.writerow(['id', 'name'])

    with open('./norm_csv/market.csv', 'w') as csvf2:
        writer = csv.writer(csvf2)
        writer.writerow(['id', 'name'])

    with open('./norm_csv/fruit_location.csv', 'w') as csvf2:
        writer = csv.writer(csvf2)
        writer.writerow(['fruit_id', 'location_id'])

if __name__ == '__main__':
    init()
    name_id = load_name_id()

    get_fruit_month_csv(name_id)
    get_monthly_history_price_csv(name_id)
    get_daily_history_price_csv(name_id)
    get_location_csv(name_id)
    get_market_csv(name_id)
    get_fruit_location_csv(name_id)