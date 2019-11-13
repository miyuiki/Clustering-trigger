import bookrollDB
import pandas as pd
import os

def get_data(course_name):
    # lines = []
    # formatted_contents = []
    # formatted_fields = []
    # with open(contents_list_file, 'r', encoding='utf-8') as fp1:
    #     lines = fp1.readlines()
    #     for line in lines:
    #         line = line.strip()
    #         formatted_contents.append(line)

    # with open(field_list_file, 'r', encoding='utf-8') as fp2:
    #     lines = fp2.readlines()
    #     for line in lines:
    #         line = line.strip()
    #         formatted_fields.append(line)
    
    # contents_list_str = ','.join(formatted_contents)
    # field_list_str = ','.join(formatted_fields)
    
    # query1 = "SET @contents_list = ('{}');".format(contents_list_str)
    # query2 = "select {} from bookroll.br_event_log where find_in_set(contents_name, @contents_list) > 0;".format(field_list_str)
    course_name = '\'' + course_name + '\''
    query = "SELECT log.user_id, log.contents_id, log.contents_name, log.operation_date, log.operation_name, c.parent_id, d.directory_id, d.name \
            FROM bookroll.br_event_log as log, bookroll.br_contents as c, bookroll.br_contents_directory as d \
            where c.parent_id = d.directory_id and c.contents_id = log.contents_id and d.name = {};".format(course_name)

    host = os.getenv('SSH_HOST')
    port = os.getenv('MYSQL_PORT')
    ssh_user = os.getenv('SSH_USER')
    ssh_password = os.getenv('SSH_PASSWORD')
    db_user = os.getenv('MYSQL_USER')
    db_password = os.getenv('MYSQL_PASSWORD')
    # query = [query1, query2]

    data = bookrollDB.connect_and_excute(host, port, ssh_user, ssh_password, db_user, db_password, query)

    return data

def preprocess(data):
    print('number of log : ' + str(len(data)))
    logs = []
    for log in data:
        logs.append(list(log))
    cols = ['user_id', 'contents_id', 'contents_name', 'operation_date', 'operation_name', 'parent_id', 'directory_id', 'name']
    df = pd.DataFrame(logs, columns=cols)
    raw = df[['user_id', 'operation_name']]
    pivot = pd.pivot_table(raw, index='user_id', columns='operation_name', aggfunc=len, fill_value=0)
    return pivot