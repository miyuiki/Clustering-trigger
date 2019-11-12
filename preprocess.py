import bookrollDB
import pandas as pd
import os

def get_data(contents_list_file, field_list_file):
    lines = []
    formatted_contents = []
    formatted_fields = []
    with open(contents_list_file, 'r', encoding='utf-8') as fp1:
        lines = fp1.readlines()
        for line in lines:
            line = line.strip()
            formatted_contents.append(line)

    with open(field_list_file, 'r', encoding='utf-8') as fp2:
        lines = fp2.readlines()
        for line in lines:
            line = line.strip()
            formatted_fields.append(line)
    
    contents_list_str = ','.join(formatted_contents)
    field_list_str = ','.join(formatted_fields)

    
    query1 = "SET @contents_list = ('{}');".format(contents_list_str)
    query2 = "select {} from bookroll.br_event_log where find_in_set(contents_name, @contents_list) > 0;".format(field_list_str)

    host = os.getenv('SSH_HOST')
    port = os.getenv('SSH_PORT')
    ssh_user = os.getenv('SSH_USER')
    ssh_password = os.getenv('SSH_PASSWORD')
    db_user = os.getenv('MYSQL_USER')
    db_password = os.getenv('MYSQL_PASSWORD')
    query = [query1, query2]

    data = bookrollDB.connect_and_excute(host, port, ssh_user, ssh_password, db_user, db_password, query)

    return data, formatted_fields

def preprocess(data, fields):
    print('number of log : ' + str(len(data)))
    logs = []
    for log in data:
        logs.append(list(log))
    df = pd.DataFrame(logs, columns=fields)
    raw = df[['user_id', 'operation_name']]
    pivot = pd.pivot_table(raw, index='user_id', columns='operation_name', aggfunc=len, fill_value=0)
    return pivot