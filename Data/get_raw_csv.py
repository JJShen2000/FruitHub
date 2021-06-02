from curses.ascii import isdigit
import datetime
import requests
from datetime import date
import os
import csv
import sys
import re

def load_name_id():
    with open('fruit.csv', 'r') as csvf:
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
                alt_date = str(int(item['交易日期'][:3])+1911) + '_' + item['交易日期'][4:6] + '_' + item['交易日期'][7:]
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

    if len(sys.argv) > 1:
        td_year = int(sys.argv[1][:4])
        td_month = int(sys.argv[1][5:7])
        td_day = int(sys.argv[1][8:])
        td = date(td_year, td_month, td_day)
    else:
        init()
        td = date.today()
        td_year = td.year
        td_month = td.month
        td_day = td.day

    #############################################################################################################

#    if len(sys.argv) > 1 and (sys.argv[-1] == 'daily_trade' or sys.argv[-1] == 'all'):
#        today_date = str(td_year-1911) + '.' + "{:0>2d}".format(td_month) + '.' + "{:0>2d}".format(td_day)
#        daily_trade_crop_to_csv(today_date, "https://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx")
#    else:    
#        temp_date = td
#
#        for d in range(5*365+3):
#            temp_date = temp_date - one_day
#
#            temp_year = temp_date.year
#            temp_month = temp_date.month
#            temp_day = temp_date.day
#
#            today_date = str(temp_year-1911) + '.' + "{:0>2d}".format(temp_month) + '.' + "{:0>2d}".format(temp_day)
#            daily_trade_crop_to_csv(today_date, "https://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx")

    #############################################################################################################

    if len(sys.argv) > 1 and (sys.argv[-1] == 'monthly_trade' or sys.argv[-1] == 'all'):
        monthly_trade_crop_to_csv(str(td_year), "https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx")
    else:
        temp_date = td

        for y in range(5+1):
            temp_date = temp_date - one_year

            temp_year = temp_date.year
            temp_month = temp_date.month
            temp_day = temp_date.day

            monthly_trade_crop_to_csv(str(temp_year), "https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx")

    #############################################################################################################

    monthly_produce_fruit_to_csv("https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx")

    #############################################################################################################

    if len(sys.argv) > 1 and (sys.argv[-1] == 'yearly_produce' or sys.argv[-1] == 'all'):
        yearly_produce_fruit_to_csv(str(td_year), "https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx")
    else:
        temp_date = td

        for y in range(5+1):
            temp_date = temp_date - one_year

            temp_year = temp_date.year
            temp_month = temp_date.month
            temp_day = temp_date.day
            
            yearly_produce_fruit_to_csv(str(temp_year), "https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx")

    #############################################################################################################
    
