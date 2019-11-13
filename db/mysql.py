import pymysql
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy

def write_df_to_mysql(df, table):
    engine = create_engine('mysql+pymysql://root:Kslab35356!@140.115.53.158:3306/kmeans')
    if table == 'ID_CLASS' or table == 'PIVOT':
        df.to_sql(name=table, con=engine, if_exists='replace', dtype={'user_id': sqlalchemy.types.VARCHAR(df.index.get_level_values('user_id').str.len().max())})
    else:
        df.to_sql(name=table, con=engine, if_exists='replace', dtype={'operation_name': sqlalchemy.types.VARCHAR(df.index.get_level_values('operation_name').str.len().max())})


# def get_conn():
#     conn = pymysql.connect(host='140.115.53.158', port=3306, user='root', passwd='Kslab35356!', db='kmeans', charset='utf8')
#     return conn

# def insert(cur, sql, args):
#     cur.execute(sql, args)

# def read_csv_to_mysql(filename):
#     with codecs.open(filename=filename, mode='r', encoding='utf-8') as f:
#         reader = csv.reader(f)
#         head = next(reader)
#         conn = get_conn()
#         cur = conn.cursor()
#         sql = 'insert into tb_csv values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#         for item in reader:
#             if item[1] is None or item[1] == '': # item[1]作為唯一鍵，不能為null
#                 continue
#         args = tuple(item)
#         print(args)
#         insert(cur, sql=sql, args=args)
#         conn.commit()
#         cur.close()
#         conn.close()