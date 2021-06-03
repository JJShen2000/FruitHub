# Data

## Usage:

* Run **get_id_name_csv.py** first 
``` 
python3 get_id_name_table.py
```
* then, run **get_raw_csv.py**  
```
python3 get_raw_tables.py 
```
* last, run **get_norm_csv.py**
```
python3 get_norm_csv.py
```

Execute get_norm_csv.py will automatically update data (start from last update or 5 years ago to current date)

## Misc
* **If no argument, it'll fetch data last 5 years.**
* 由於拿API的全部資料需要辦帳號, 所以fruit_id我是用**農產品交易行情**的過去五年內所有出現作物來記錄的
* 由於有出現像是椰子，椰子-剝殼這種情形，所以我只取關鍵字，像是這個我就只留椰子，然後只保留椰子的fruit_id
* Feel free to make any changes

## TODO
* Find smarter way to make fruit's id_name table
* Speed up updating norm_csv.
* Make some changes to let the program more easier to use (?
* Write a shell script to update automatically (?
