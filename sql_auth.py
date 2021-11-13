Env = 'testsqlal'

if Env == 'live':

    app ={
        'name' : 'mysql+pymysql',
        'user' : '----',
        'password': '----',
        'host': '0.0.0.0',
        'db': 'Account',
        'port': ''
    }
elif Env == 'test' :

    app = {
        'name': 'mysql+pymysql',
        'user': '----',
        'password': '----',
        'host': '127.0.0.1',
        'db': 'Account',
        'port': ''
    }
