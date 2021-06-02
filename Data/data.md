# Data

## Usage:

* Run **get_id_name_table.py** first 
``` 
python3 get_id_name_table.py
```
* then, run **get_raw_tables.py**  
```
python3 get_raw_tables.py [date(yyyy.mm.dd)] [update option]
```

Three update options
1. daily_trade: update the csv **DailyTrade.csv** based on the given date
2. monthly_trade: update the csv **MonthlyTrade.csv** based on the given date
3. yearly_produce: update the csv **YearlyProduce.csv** based on the given date

e.g.  
python3 get_raw_tables.py 2015_07_13 monthly_trade  
will insert data from 2015 into **MonthlyTrade.csv**

## Misc
* **If no argument, it'll fetch data last 5 years.**
* 由於拿API的全部資料需要辦帳號, 所以fruit_id我是用**農產品交易行情**的過去五年內所有出現作物來記錄的
* 由於有出現像是椰子，椰子-剝殼這種情形，所以我只取關鍵字，像是這個我就只留椰子，然後只保留椰子的fruit_id
* 還沒normalized(也就是像hackmd上面那樣分成很多table)
* I did not test the **update option** yet
* Not yet deal with the duplicate scenario (might happen when inserting data already exist)
* Feel free to make any changes
