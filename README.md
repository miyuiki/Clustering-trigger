# Clustering trigger
## Features
可從BookRoll Mysql 撈取指定教材和指定欄位資料，並將前處理資料以及k-means分析完成的資料傳送至MongoDB
## Requirements
1. pymysql
2. sshtunnel
3. pandas
4. sklearn
5. numpy
6. pymongo
7. pymysql
8. sqlalchemy
## Usage
修改run.sh填入所需的變數，並在參數列指定需要撈取的教材，執行`sh run.sh`即可，
若只需要連線至Mysql並作前處理可以用以下程式碼
```python
import preprocess
data = preprocess.getdata(course_name=args.course_name)
```
