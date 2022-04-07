from scripts.query_builder import *
import pyodbc
from scripts.env import DATABASE, DRIVER, PASSWORD, PORT, SERVER, USERNAME

def user_auth(email, password):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_user_auth_query(email, password))
                result = cursor.fetchall()
                if (email == result[0][0] and password == result[0][1]):
                    return True
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def pin_reset(email, old_pin, new_pin, new_pin2):
    if new_pin == new_pin2:
        if user_auth(email, old_pin):
            try: 
                with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(get_pin_reset_query(email, new_pin))
                        return True
            except Exception as e:
                print("Ocurrió un error al conectar a SQL Server: ", e)
                return False
        else:
            return False
    else:
        return False
        
def get_flights(day, month, operator, departament):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_flights_query(day, month, operator, departament))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False
