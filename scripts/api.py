from env import *
import pyodbc
from env import DATABASE, DRIVER, PASSWORD, SERVER, USERNAME

def user_auth(email, password):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT pin FROM usuarios WHERE usuario ='" + email + "' And pin ='" + password + "';")
                result = cursor.fetchall()
                print(result)
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)

print(user_auth('programadorit@laats.net', '7070'))
