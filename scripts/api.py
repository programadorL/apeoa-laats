from scripts.query_builder import *
import pyodbc
import scripts.env
from scripts.env import DATABASE, DRIVER, PASSWORD, PORT, SERVER, USERNAME, USER_ID, DEPARTMENT

def user_auth(email, password):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_user_auth_query(email, password))
                result = cursor.fetchall()
                if (email == result[0][0] and password == result[0][1]):
                    scripts.env.USER_ID = result[0][2]
                    scripts.env.DEPARTMENT = get_department(scripts.env.USER_ID)
                    scripts.env.set_department_color()
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

def get_department(user_id):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_department_query(user_id))
                result = cursor.fetchall()
                return result[0][0]
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_operators():
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_operators_query())
                result = cursor.fetchall()
                print(result)
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False
