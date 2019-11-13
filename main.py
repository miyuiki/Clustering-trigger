import preprocess
import classifier
import pandas as pd
import db.mongoDB
import os
from db.mysql import write_df_to_mysql
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--course-name', dest="course_name")
parser.add_argument('--use-mongo', dest="use_mongo")
parser.add_argument('--use-mysql', dest="use_mysql")

args = parser.parse_args()

raw_data = preprocess.get_data(course_name=args.course_name)

use_mysql = True if args.use_mysql == 'true' else False
use_mongo = True if args.use_mongo == 'true' else False

data = preprocess.preprocess(data=raw_data)
data.to_json('output/preprocessed.json', orient='index')

if use_mysql:
    write_df_to_mysql(df=data, table='PIVOT')
# print(data)

centers_k3, label_k3 = classifier.run_clustering(df=data, k=3)
centers_k4, label_k4 = classifier.run_clustering(df=data, k=4)
centers_k5, label_k5 = classifier.run_clustering(df=data, k=5)

k3_df = classifier.get_class_df(df=data, label=label_k3, col_name='k3_label')
k4_df = classifier.get_class_df(df=data, label=label_k4, col_name='k4_label')
k5_df = classifier.get_class_df(df=data, label=label_k5, col_name='k5_label')

class_df = k3_df.join(k4_df).join(k5_df)
if use_mysql:
    write_df_to_mysql(df=class_df, table='ID_CLASS')
class_df.to_json('output/class_df.json', orient='index')

k3_centers = classifier.get_center_df(df=data, centers=centers_k3.T, class_num=3)
k4_centers = classifier.get_center_df(df=data, centers=centers_k4.T, class_num=4)
k5_centers = classifier.get_center_df(df=data, centers=centers_k5.T, class_num=5)

if use_mysql:
    write_df_to_mysql(df=k3_centers, table='K3_CENTERS')
    write_df_to_mysql(df=k4_centers, table='K4_CENTERS')
    write_df_to_mysql(df=k5_centers, table='K5_CENTERS')
k3_centers.to_json('output/k3_centers.json', orient='index')
k4_centers.to_json('output/k4_centers.json', orient='index')
k5_centers.to_json('output/k5_centers.json', orient='index')

#write data to mongodb
if use_mongo:
    client = mongoDB.connect(host=os.getenv('MONGO_HOST'), port='27017', username=os.getenv('MONGO_USER'), password=os.getenv('MONGO_PASSWORD'))
    mongoDB.update(client, 'preprocessed_data', 'output/preprocessed.json')
    mongoDB.update(client, 'id_clustering', 'output/class_df.json')
    mongoDB.update(client, 'k3_centers', 'output/k3_centers.json')
    mongoDB.update(client, 'k4_centers', 'output/k4_centers.json')
    mongoDB.update(client, 'k5_centers', 'output/k5_centers.json')