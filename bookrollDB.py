from sshtunnel import SSHTunnelForwarder
import pymysql

def connect_and_excute(host, port, ssh_user, ssh_password, db_user, db_password, query):
    data = []
    with SSHTunnelForwarder(ssh_address_or_host=(host, 22), ssh_username=ssh_user, ssh_password=ssh_password, remote_bind_address=('127.0.0.1', port)) as server:
        db = 'bookroll'
        myConfig = pymysql.connect(user=db_user, passwd=db_password, host="127.0.0.1", db=db, port=server.local_bind_port)
        cursor = myConfig.cursor()
        for q in query:
            cursor.execute(q)
        data = list(cursor.fetchall())
    
        cursor.close()

        # return all fetched data
        return data 