from curses.ascii import isdigit
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

def daily_trade_crop_to_csv(date, url):
    url += "?$StartDate=" + date + '&EndDate=' + date
    data = requests.get(url).json()

    with open('./raw_csv/DailyTrade.csv', 'a') as csvf:
        writer = csv.writer(csvf)

        name_id = load_name_id()

        for item in data:
            temp = ''
            for w in item['作物名稱']:
                if w == '-':
                    break
                else:
                    temp += w if re.search("[\u4e00-\u9FFF]", w) else ''

            if name_id.get(temp) != None:
                alt_date = str(int(item['交易日期'][:3])+1911) + '-' + item['交易日期'][4:6] + '-' + item['交易日期'][7:]
                writer.writerow([alt_date, temp, int(item['市場代號']), item['市場名稱'], float(item['平均價']), float(item['交易量'])])

def monthly_trade_crop_to_csv(year, url):    
    url += "?UnitID=652&$filter=年份+like+" + year
    data = requests.get(url).json()

    with open('./raw_csv/MonthlyTrade.csv', 'a') as csvf:
        writer = csv.writer(csvf)
        
        for item in data:
            for key in item:
                if key == '作物':
                    temp = ''
                    for w in item[key]:
                        if w == '(':
                            break
                        else:
                            temp += w if re.search("[\u4e00-\u9FFF]", w) else ''
                    item[key] = temp

                if key != '作物' and ((type(item[key]) != str) or (len(item[key]) == 0) or (not item[key][0].isdigit())):
                    item[key] = ''

            writer.writerow([item['作物'], int(item['年份'][:-1]), item['1月價格'], item['2月價格'], item['3月價格'], item['4月價格'], \
                             item['5月價格'], item['6月價格'], item['7月價格'], item['7月價格'], item['8月價格'], item['9月價格'],      \
                             item['10月價格'], item['11月價格'], item['12月價格']])


def monthly_produce_fruit_to_csv(url):
    url += "?UnitId=061&$filter=type+like+水果"
    data = requests.get(url).json()

    with open('./raw_csv/MonthlyProcudeFruit.csv', 'a') as csvf:
        writer = csv.writer(csvf)

        for item in data:
            writer.writerow([int(item['month']), item['crop'], item['variety'] if len(item['variety']) > 0 else '', item['county'], item['town']])


def yearly_produce_fruit_to_csv(year, url):
    url += "?UnitId=135&$filter=年度+like+" + year
    data = requests.get(url).json()

    with open('./raw_csv/YearlyProcudeFruit.csv', 'a') as csvf:
        writer = csv.writer(csvf)

        for item in data:
            writer.writerow([int(item['年度']), item['地區別'], item['果品類別'], float(item['產量_公噸']) if item['產量_公噸'][0].isdigit() else ""])

def init():
    if not os.path.isdir('./raw_csv'):
        os.mkdir("./raw_csv")


    with open('./raw_csv/DailyTrade.csv', 'w') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['date', 'fruit_name', 'market_id', 'market_name', 'price', 'transaction'])

    with open('./raw_csv/MonthlyTrade.csv', 'w') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['fruit_name', 'year', 'January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    with open('./raw_csv/MonthlyProcudeFruit.csv', 'w') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['month', 'fruit_name', 'Variety', 'County', 'Town'])

    with open('./raw_csv/YearlyProcudeFruit.csv', 'w') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['year', 'County', 'fruit_name', 'Production'])

if __name__ == "__main__":

    name_id = load_name_id()

    one_day = datetime.timedelta(days=1)
    one_year = datetime.timedelta(days=365)
    
    td = date.today()
    td_year = td.year
    td_month = td.month
    td_day = td.day

    update = False
    daily_st = date.today() - 5*one_year
    monthly_st = date.today() - 5*one_year
    yearly_st = date.today() - 5*one_year

    daily_ld = td
    monthly_ld = td
    yearly_ld = td

    if not os.path.isfile('./raw_csv/update.log'):
        with open('./raw_csv/update.log', 'w') as ulog:
            ulog.write(str(td)+'\n')
            ulog.write(str(td)+'\n')
            ulog.write(str(td)+'\n')
        init()
    else:
        with open('./raw_csv/update.log', 'r') as ulog:
            ld = ulog.readline()
            if date(int(ld[:4]), int(ld[5:7]), int(ld[8:10])) < td:
                update = True
                daily_st = date(int(ld[:4]), int(ld[5:7]), int(ld[8:10])) +  one_day
            else:
                daily_ld = date(int(ld[:4]), int(ld[5:7]), int(ld[8:10]))
                daily_st = td

            ld = ulog.readline()
            if date(int(ld[:4]), int(ld[5:7]), int(ld[8:10])) +  one_year <= td:
                update = True
                monthly_st = date(int(ld[:4]), int(ld[5:7]), int(ld[8:10])) +  one_year
            else:
                monthly_ld = date(int(ld[:4]), int(ld[5:7]), int(ld[8:10]))
                monthly_st = td

            ld = ulog.readline()
            if date(int(ld[:4]), int(ld[5:7]), int(ld[8:10])) + one_year <= td:
                update = True
                yearly_st = date(int(ld[:4]), int(ld[5:7]), int(ld[8:10])) +  one_year
            else:
                yearly_ld = date(int(ld[:4]), int(ld[5:7]), int(ld[8:10]))
                yearly_st = td

        if update:
            with open('./raw_csv/update.log', 'w') as ulog:
                ulog.write(str(daily_ld)+'\n')
                ulog.write(str(monthly_ld)+'\n')
                ulog.write(str(yearly_ld)+'\n')

    #############################################################################################################

    temp_date = daily_st

    while temp_date < td:
        temp_year = temp_date.year
        temp_month = temp_date.month
        temp_day = temp_date.day

        today_date = str(temp_year-1911) + '.' + "{:0>2d}".format(temp_month) + '.' + "{:0>2d}".format(temp_day)
        daily_trade_crop_to_csv(today_date, "https://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx")

        temp_date = temp_date + one_day
    #############################################################################################################

    temp_date = monthly_st

    while temp_date < td:
        temp_year = temp_date.year
        temp_month = temp_date.month
        temp_day = temp_date.day

        monthly_trade_crop_to_csv(str(temp_year), "https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx")

        temp_date = temp_date + one_year
    #############################################################################################################

    monthly_produce_fruit_to_csv("https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx")

    #############################################################################################################

    temp_date = yearly_st

    while temp_date < td:
        temp_year = temp_date.year
        temp_month = temp_date.month
        temp_day = temp_date.day
        
        yearly_produce_fruit_to_csv(str(temp_year), "https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx")

        temp_date = temp_date + one_year
    #############################################################################################################
    
