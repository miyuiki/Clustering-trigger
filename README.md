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
## Usage
將需要撈取的教材名稱寫在`contents.txt`中，需要撈取的欄位寫在`fields.txt`中，若只需要連線至Mysql並作前處理可以用以下程式碼
`import preprocess`
`data = preprocess.getdata('contents.txt', 'fields.txt')`
