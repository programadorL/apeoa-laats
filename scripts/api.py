from env import *
import pyodbc
from env import DATABASE, DRIVER, PASSWORD, SERVER, USERNAME
#test comment
def user_auth(email, password):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT usuario, pin FROM usuarios WHERE usuario ='" + email + "' And pin ='" + password + "';")
                result = cursor.fetchall()
                if (email == result[0][0] and password == result[0][1]):
                    return True
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

print(user_auth('programadorit@laats.net', '7070'))

def get_flights(date):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT usuario, pin FROM usuarios WHERE usuario ='" + email + "' And pin ='" + password + "';")
                result = cursor.fetchall()
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False