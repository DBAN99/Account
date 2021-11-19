Env = 'test'

if Env == 'live':

    app ={
        'name' : 'mysql+pymysql',
        'user' : '----',
        'password': '----',
        'host': '0.0.0.0',
        'dbconn': 'Account',
        'port': ''
    }
elif Env == 'test' :

    app = {
        'name': 'mysql+pymysql',
        'user': 'root',
        'password': '1234',
        'host': '127.0.0.1',
        'dbconn': 'request',
        'port': '3306'
    }
