from pymongo import MongoClient
import json

def connect(host, port, username, password):
    cursor = None
    client = MongoClient('mongodb://{}:{}@{}:{}/'.format(username, password, host, port))
    try:
        print(client.server_info())
        print('\n----------------------------\nMongoDB connection created successfully')
        cursor = client.BR_CLUSTERING
    except:
        print('Failed to create MongoDB connection')

    return cursor

def update(cursor, collection_name, file_path):
    collection = cursor[collection_name]
    collection.delete_many({})
    with open(file_path, 'r') as data_file:
        data_json = json.load(data_file)
        collection.insert(data_json)
