import datetime
from datetime import date
import requests
import csv
import sys
import re
import os

one_day = datetime.timedelta(days=1)
id_name = {}

def get_id_name(date, url):
    for d in range(365*5+1):
        str_date = str(int(date.year-1911)) + '.' + "{:0>2d}".format(date.month) + '.' + "{:0>2d}".format(date.day)
        print(str_date)
        curl = url + "?$StartDate=" + str_date + '&EndDate=' + str_date
        data = requests.get(curl).json()

        for item in data:
            temp = ''
            
            for w in item['作物名稱']:
                if w == '-':
                    break
                else:
                    temp += w if re.search("[\u4e00-\u9FFF]", w) else ''
            
            if id_name.get(temp) == None and item['種類代碼'] == "N05":
                id_name[temp] = item['作物代號']
            
        date = date - one_day
    
    with open('./norm_csv/fruit.csv', 'w') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['id', 'name'])

        for key in id_name:
            writer.writerow([id_name[key], key])


if __name__ == "__main__":

    if len(sys.argv[1:]) > 0:
        td_year = int(sys.argv[-1][:4])
        td_month = int(sys.argv[-1][5:7])
        td_day = int(sys.argv[-1][8:])
        td = date(td_year, td_month, td_day)
    else:
        td = date.today()

    if not os.path.isdir('./norm_csv'):
        os.mkdir("./norm_csv")

    get_id_name(td, "https://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx")