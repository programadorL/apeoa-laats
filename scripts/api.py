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
                    scripts.env.LOGGED_IN = True
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
        
def get_flights(day, month, year, department):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_flights_query(day, month, year, department))
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

def get_operator_id(operator_name):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_operator_id_query(operator_name))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_operators():
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_operators_query())
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_aircraft_id(aircraft, operator_id):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_aircraft_id_query(aircraft, operator_id))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_aircrafts(id_operator):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_aircrafts_query(id_operator))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_personel_parameters_pxs(operation_type, aircraft_id):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_personel_parameters_pxs_query(operation_type, aircraft_id))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_specific_flight(day, month, year, department, operation_type, operator, aircraft_type):
    print(get_specific_flight_query(day, month, year, department, operation_type, operator, aircraft_type))
    try:
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_specific_flight_query(day, month, year, department, operation_type, operator, aircraft_type))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_flight_personel_parameters_pxs(operation_type, aircraft_id):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_flight_personel_parameters_pxs_query(operation_type, aircraft_id))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_flight_personel_configuration_pxs(no_correlative):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_flight_personel_configuration_pxs_query(no_correlative))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_flight_et_personel_parameters_pxs(parameter_id):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_flight_et_personel_parameters_pxs_query(parameter_id))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_flight_times_personel_pxs(parameter_id):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_flight_times_personel_pxs_query(parameter_id))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_flight_by_correlative(no_correlative):
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_flight_by_correlative_query(no_correlative))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False