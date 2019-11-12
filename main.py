import preprocess
import classifier
import pandas as pd
import mongoDB

raw_data, fields = preprocess.get_data('contents.txt', 'fields.txt')
data = preprocess.preprocess(data=raw_data, fields=fields)
data.to_json('output/preprocessed.json', orient='index')

centers_k3, label_k3 = classifier.run_clustering(df=data, k=3)
centers_k4, label_k4 = classifier.run_clustering(df=data, k=4)
centers_k5, label_k5 = classifier.run_clustering(df=data, k=5)

k3_df = classifier.get_class_df(df=data, label=label_k3, col_name='k3_label')
k4_df = classifier.get_class_df(df=data, label=label_k4, col_name='k4_label')
k5_df = classifier.get_class_df(df=data, label=label_k5, col_name='k5_label')

class_df = k3_df.join(k4_df).join(k5_df)
class_df.to_json('output/class_df.json', orient='index')

k3_centers = classifier.get_center_df(df=data, centers=centers_k3.T, class_num=3)
k4_centers = classifier.get_center_df(df=data, centers=centers_k4.T, class_num=4)
k5_centers = classifier.get_center_df(df=data, centers=centers_k5.T, class_num=5)

k3_centers.to_json('output/k3_centers.json', orient='index')
k4_centers.to_json('output/k4_centers.json', orient='index')
k5_centers.to_json('output/k5_centers.json', orient='index')

#write data to mongodb
client = mongoDB.connect(host='140.115.53.147', port='27017', username='readWrite_user', password='kslab_readwrite')
mongoDB.update(client, 'preprocessed_data', 'preprocessed.json')
mongoDB.update(client, 'id_clustering', 'class_df.json')
mongoDB.update(client, 'k3_centers', 'k3_centers.json')
mongoDB.update(client, 'k4_centers', 'k4_centers.json')
mongoDB.update(client, 'k5_centers', 'k5_centers.json')