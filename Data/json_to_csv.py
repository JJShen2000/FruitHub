from curses.ascii import isdigit
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
import json
import csv
import sys
import re

driver = webdriver.Firefox()

def get_json(url):
    driver.get(url)
    psrc = driver.page_source
    bs = BeautifulSoup(psrc, "html.parser")
    js = json.loads(bs.text)

    return js

def daily_trade_crop_to_csv(date, url):
    url += "?$StartDate=" + date + '&EndDate=' + date
    data = get_json(url)

    with open('DailyTrade.csv', 'w') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['Date', 'CropName', 'MarketID', 'MarketName', 'AvgPrice', 'Transaction'])

        for item in data:
            alt_date = str(int(item['交易日期'][:3])+1911) + item['交易日期'][3:]
            writer.writerow([alt_date, item['作物名稱'], int(item['市場代號']), item['市場名稱'], float(item['平均價']), float(item['交易量'])])

def monthly_trade_crop_to_csv(year, url):
    url += "?UnitID=652&$filter=年份+like+" + year
    data = get_json(url)

    with open('MonthlyTrade.csv', 'w') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['CropName', 'Year', 'January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

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
                    item[key] = float(-1)

            writer.writerow([item['作物'], int(item['年份'][:-1]), float(item['1月價格']), float(item['2月價格']), float(item['3月價格']), float(item['4月價格']), float(item['5月價格']), float(item['6月價格']), float(item['7月價格']), float(item['7月價格']), float(item['8月價格']), float(item['9月價格']), float(item['10月價格']), float(item['11月價格']), float(item['12月價格'])])

def monthly_produce_fruit_to_csv(url):
    url += "?UnitId=061&$filter=type+like+水果"
    data = get_json(url)

    with open('MonthlyProcudeFruit.csv', 'w') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['Month', 'CropName', 'Variety', 'County', 'Town'])

        for item in data:
            writer.writerow([int(item['month']), item['crop'], item['variety'] if len(item['variety']) > 0 else 'NULL', item['county'], item['town']])

def yearly_produce_fruit_to_csv(year, url):
    url += "?UnitId=135&$filter=年度+like+" + year
    data = get_json(url)


    with open('YearlyProcudeFruit.csv', 'w') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['Year', 'County', 'CropName', 'Production'])

        for item in data:
            writer.writerow([int(item['年度']), item['地區別'], item['果品類別'], float(item['產量_公噸']) if item['產量_公噸'][0].isdigit() else "NULL"])

if __name__ == "__main__":

    if len(sys.argv[1:]) > 0:
        td_year = int(sys.argv[-1][:4])
        td_month = int(sys.argv[-1][5:7])
        td_day = int(sys.argv[-1][8:])
    else:
        td = date.today()
        td_year = td.year
        td_month = td.month
        td_day = td.day

    #############################################################################################################

    today_date = str(td_year-1911) + '.' + "{:0>2d}".format(td_month) + '.' + "{:0>2d}".format(td_day)
    daily_trade_crop_to_csv(today_date, "https://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx")

    #############################################################################################################

    monthly_trade_crop_to_csv(str(td_year), "https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx")

    #############################################################################################################

    monthly_produce_fruit_to_csv("https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx")

    #############################################################################################################

    yearly_produce_fruit_to_csv(str(td_year), "https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx")

    driver.close()

    