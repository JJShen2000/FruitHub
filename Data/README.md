# Data

## Usage:

* run shell script **update.sh**
```
chmod u+x update.sh

./update.sh
```

* Use **crontab** to execute **update.sh** to update data daily.

## Misc
* **If no argument, it'll fetch data last 5 years.**
* 由於拿API的全部資料需要辦帳號, 所以fruit_id我是用**農產品交易行情**的過去五年內所有出現作物來記錄的
* 由於有出現像是椰子，椰子-剝殼這種情形，所以我只取關鍵字，像是這個我就只留椰子，然後只保留椰子的fruit_id
* Feel free to make any changes

## TODO
* Find smarter way to make fruit's id_name table
* Speed up updating norm_csv.
* Make some changes to let the program more easier to use (?