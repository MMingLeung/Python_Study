from core import client
from lib import auth, db_handle

def run():
    '主逻辑'
    while True:
        try:
            client_obj, username, quota = client.FTP_Client
            msg = '''
            =======Welcome FTP Sevice======
            1.download/upload/ls
            2.Please looking forward to...<------desgining----->
            '''
            print(msg)
            choice = input("Please input your choice:  ")
            if choice == '1':
                client_obj.client_conn

                client_obj.run(username, quota)
            elif choice == '2':
                pass
        except Exception:
            break
