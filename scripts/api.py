'''
    @Author: Esteban Cabrera.
    @Version: 1.0.0.
    @See: query_builder.py.

    Este script contiene métodos creados para generar los queries a ejecutar en la base de datos
    para obtener la información deseada a base de parámetros establecidos.
'''

from scripts.query_builder import *
import pyodbc
import scripts.env
from scripts.env import DATABASE, DRIVER, PASSWORD, PORT, SERVER, USERNAME, USER_ID, DEPARTMENT

def user_auth(email, password):
    '''
        Este metodo se utiliza para validar la autenticidad del usuario que desea ingresar a la App. 

        Parametros:
            email -> string
            password -> int *Hace referencia al PIN del usuario*

        Ver en query_builder.py:
            get_user_auth_query(<args>)
        
        Salida (Bool):
            True: El usuario esta autorizado.
            False: El usuario NO esta autorizado o no es valido.
    '''
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
    '''
        Este metodo se utiliza para actualizar el PIN (PERSONAL IDENTIFICATION NUMBER) del usuario. 

        Parametros:
            email -> string
            old_pin -> int
            new_pin -> int
            new_pin2 - > int *Es la confirmacion del nuevo ping*

        Ver en query_builder.py:
            get_pin_reset_query(<args>)
        
        Salida (Bool):
            True: Se actualizo el PIN correctamente.
            False: No se pudo actualizar el PIN.
    '''
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
    '''
        Este metodo se utiliza para obtener un dataset de vuelos basado en el dia, mes, año de realizacion
        y departamento al que pertenecen las operaciones. 

        Parametros:
            day -> int
            month -> int
            year -> int
            department -> string

        Ver en query_builder.py:
            get_flights_query(<args>)
        
        Salida (Array):
            [
                <dia>, <mes>, <year>, <origen>, <destino>,
                <hora_ingreso>, <hora_egreso>, <no_vuelo>, <operador>, 
                <no_correlativo>, <tipo_aeronave>
            ]
    '''
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
    '''
        Este metodo se utiliza para obtener el nombre del departamento al que un usuario pertenece.

        Parametros:
            user_id -> int

        Ver en query_builder.py:
            get_department_query(<arg>)
        
        Salida (string):
            nombre_operador ej. "AMERICAN"
    '''
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
    '''
        Este metodo se utiliza para obtener el identificador unico de un operador especifico por medio
        del nombre.

        Parametros:
            operator_name -> string

        Ver en query_builder.py:
            get_operator_id_query(<arg>)
        
        Salida (int):
            id_operador ej. 1
    '''
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
    '''
        Este metodo se utiliza para obtener un dataset de todos los operadores. 

        Ver en query_builder.py:
            get_operators_query(<args>)
        
        Salida (Array):
            [
                <id_operador>, <nombre_operador>, <id_secondary>
            ]
    '''
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
    '''
        Este metodo se utiliza para obtener el identificador unico de una aeronave especifica por medio
        del tipo y el identificador de uno de los operadores.

        Parametros:
            aircraft -> string
            operator_id -> int

        Ver en query_builder.py:
            get_aircraft_id_query(<arg>)
        
        Salida (int):
            id_aeronave ej. 1
    '''
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
    '''
        Este metodo se utiliza para obtener un dataset de todos las aeronaves que coincidan con
        el identificador de uno de los operadores.

        Parametros:
            id_operator -> int

        Ver en query_builder.py:
            get_aircrafts_query(<arg>)
        
        Salida (Array):
            [
                <id_aeronave>, <tipo_aeronave>, <operador>
            ]
    '''
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_aircrafts_query(id_operator))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_specific_flight(day, month, year, department, operation_type, operator, aircraft_type):
    '''
        Este metodo se utiliza para obtener un dataset de un itinerario de vuelo especifico basandose en
        el dia, mes, año de realizacion, departamento al que pertenece, tipo de operacion,
        operador y tipo de aeronave.

        Parametros:
            day -> int
            month -> int
            year -> int 
            department -> string
            operation_type -> string
            operator -> string
            aircraft_type -> string

        Ver en query_builder.py:
            get_specific_flight_query(<arg>)
        
        Salida (Array):
            [
                <no_correlativo>,
                <year>,
                <dia>,
                <mes>,
                <departamento>,
                <origen>,
                <destino>,
                <hora_ingreso>,
                <hora_egreso>,
                <no_vuelo>,
                <operador>,
                <tipo_operacion>,
                <fecha>,
                <borrar>,
                <tipo_aeronave>,
                <puerta>,
                <matricula>
            ]
    '''
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
    '''
        Este metodo se utiliza para obtener un dataset de los parametros de personal establecidos para 
        un tipo de vuelo especifico.

        Parametros:
            operation_type -> string
            aircraft_id -> int

        Ver en query_builder.py:
            get_flight_personel_parameters_pxs_query(<arg>)
        
        Salida (Array):
            [
                <id_parametro>,
                <aeronave>,
                <tipo_operacion>,
                <crew_chief>,
                <operador>,
                <agente_rampa>,
                <agente_mostrador>,
                <agente_fajas>,
                <agente_rayos_x>,
                <agente_limpieza>
            ]
    '''
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
    '''
        Este metodo se utiliza para obtener un dataset de la configuracion de personal automatizada
        para un vuelo especifico.

        Parametros:
            no_correlative -> int

        Ver en query_builder.py:
            get_flight_personel_configuration_pxs_query(<arg>)
        
        Salida (Array):
            [
                <no_correlativo>,
                <aeronave>,
                <crew_chief>,
                <operador>,
                <agente_rampa>,
                <agente_mostrador>,
                <agente_fajas>,
                <agente_rayos_x>,
                <agente_limpieza>
            ]
    '''
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
    '''
        Este metodo se utiliza para obtener un dataset de los parametros (banderas) de ET (estimated time)
        basados en el identificador de un parametro especifico 
        *relacionado a la tabla 'parametros_personal_pxs*.

        Parametros:
            parameter_id -> int

        Ver en query_builder.py:
            get_flight_et_personel_parameters_pxs_query(<arg>)
        
        Salida (Array):
            [
                <id_parametro>,
                <crew_chief_inicio>,
                <crew_chief_final>,
                <operador_inicio>,
                <operador_final>,
                <agente_rampa_inicio>,
                <agente_rampa_final>,
                <agente_mostrador_inicio>,
                <agente_mostrador_final>,
                <agente_fajas_inicio>,
                <agente_fajas_final>,
                <agente_rayos_x_inicio>,
                <agente_rayos_x_final>,
                <agente_limpieza_inicio>,
                <agente_limpieza_final>
            ]
    '''
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
    '''
        Este metodo se utiliza para obtener un dataset de los parametros de los tiempos (minutos),
        antes o despues del tiempo estimado (ETA o ETD) en los que el personal debe comenzar labores,
        basados en el identificador unico de un parametro especifico 
        *relacionado a la tabla 'parametros_personal_pxs*.

        Parametros:
            parameter_id -> int

        Ver en query_builder.py:
            get_flight_times_personel_pxs_query(<arg>)
        
        Salida (Array):
            [
                <id_parametro>,
                <crew_chief_inicio>,
                <crew_chief_final>,
                <operador_inicio>,
                <operador_final>,
                <agente_rampa_inicio>,
                <agente_rampa_final>,
                <agente_mostrador_inicio>,
                <agente_mostrador_final>,
                <agente_fajas_inicio>,
                <agente_fajas_final>,
                <agente_rayos_x_inicio>,
                <agente_rayos_x_final>,
                <agente_limpieza_inicio>,
                <agente_limpieza_final>
            ]
    '''
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
    '''
        Este metodo se utiliza para obtener un dataset del itinerario de un vuelo especifico
        basado en el correlativo. 

        Parametros:
            no_correlativo -> int

        Ver en query_builder.py:
            get_flight_by_correlative_query(<args>)
        
        Salida (Array):
            [
                <no_correlativo>,
                <year>,
                <dia>,
                <mes>,
                <departamento>,
                <origen>,
                <destino>,
                <hora_ingreso>,
                <hora_egreso>,
                <no_vuelo>,
                <operador>,
                <tipo_operacion>,
                <fecha>,
                <borrar>,
                <tipo_aeronave>,
                <puerta>,
                <matricula>
            ]
    '''
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_flight_by_correlative_query(no_correlative))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False

def get_configuracion_personal_pxs(no_correlative):
    '''
        Este metodo se utiliza para obtener un dataset de la configuracion de personal para un itinerario
        de vuelo especifico basado en el numero de correlativo. 
        *relacionado a la tabla 'itinerarios*.

        Parametros:
            no_correlative -> int

        Ver en query_builder.py:
            get_configuracion_personal_pxs_query(<arg>)
        
        Salida (Array):
            [
                <no_correlativo>,
                <aeronave>,
                <crew_chief>,
                <operador>,
                <agente_rampa>,
                <agente_mostrador>,
                <agente_fajas>,
                <agente_rayos_x>,
                <agente_limpieza>
            ]
    '''
    try: 
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT='+PORT+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_configuracion_personal_pxs_query(no_correlative))
                result = cursor.fetchall()
                staff_positions = ['Crew chief', "Operadores", "Agentes de rampa", "Agentes de mostrador", "Agentes de fajas", "Agentes de rayos x", "Agentes de limpieza"]
                staff_qty = []
                for i in range(2,9):
                    staff_qty.append(result[0][i])
                staff_config = [staff_positions, staff_qty]
                return staff_config
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
        return False