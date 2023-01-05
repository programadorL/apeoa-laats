'''
    @Author: Esteban Cabrera.
    @Version: 1.0.0.
    @See: api.py.

    Este script contiene métodos creados para generar los queries en el lenguaje SQL a ejecutar 
    en la base de datos para obtener la información deseada a base de parámetros establecidos.
'''

def get_user_auth_query(email, password):
    '''
        Este metodo se utiliza para generar el query que valide la autenticidad del usuario que desea
        ingresar a la App. 

        Parametros:
            email -> string
            password -> int *Hace referencia al PIN del usuario*

        Ver en api.py:
            get_user_auth(<args>)
        
        Salida (string):
            query ej. "SELECT usuario, pin, id_usuario FROM usuarios WHERE usuario =..."
    '''
    return "SELECT usuario, pin, id_usuario FROM usuarios WHERE usuario ='" + email + "' And pin ='" + password + "';"

def get_pin_reset_query(email, new_pin):
    '''
        Este metodo se utiliza para generar el query que actualiza el PIN (PERSONAL IDENTIFICATION NUMBER) 
        del usuario. 

        Parametros:
            email -> string
            new_pin -> int

        Ver en api.py:
            get_pin_reset(<args>)
        
        Salida (string):
            query ej. "UPDATE usuarios SET pin=..."
    '''
    return "UPDATE usuarios SET pin='" + new_pin + "' WHERE usuario='" + email + "';"

def get_flights_query(day, month, year, department):
    '''
        Este metodo se utiliza para generar el query que obtiene un dataset de vuelos basado 
        en el dia, mes, año de realizacion y departamento al que pertenecen las operaciones. 

        Parametros:
            day -> int
            month -> int
            year -> int
            department -> string

        Ver en api.py:
            get_flights(<args>)
        
        Salida (string):
            query ej. "SELECT dia, mes, year, origen, destino, hora_ingreso, hora_egreso, no_vuelo, operador, no_correlativo, tipo_aeronave FROM itinerarios WHERE dia=..."
    '''
    return "SELECT dia, mes, year, origen, destino, hora_ingreso, hora_egreso, no_vuelo, operador, no_correlativo, tipo_aeronave FROM itinerarios WHERE dia='"+day+"' And  mes='"+month+"' And  year='"+year+"' And departamento='"+department+"' And tipo_operacion <> 'RECEPCION' and tipo_aeronave <> '';"

def get_flight_by_correlative_query(no_correlative):
    
    return "SELECT * FROM itinerarios WHERE no_correlativo="+no_correlative+";"

def get_department_query(user_id):
    '''
        Este metodo se utiliza para generar el query que obtiene el nombre del departamento 
        al que un usuario pertenece.

        Parametros:
            user_id -> int

        Ver en api.py:
            get_department(<arg>)
        
        Salida (string):
            query ej. SELECT departamento FROM Personal_General WHERE codigo_empleado=..."
    '''
    return "SELECT departamento FROM Personal_General WHERE codigo_empleado="+str(user_id)+";"  

def get_operators_query():
    '''
        Este metodo se utiliza para generar el query que obtiene un dataset de todos los operadores. 

        Ver en api.py:
            get_operators_(<args>)
        
        Salida (string):
            query ej. "SELECT id_operador, nombre_operador FROM operadores WHERE id_operador >..."
    '''
    return "SELECT id_operador, nombre_operador FROM operadores WHERE id_operador > 1 ORDER BY nombre_operador ASC;"

def get_aircrafts_query(operator_id):
    '''
        Este metodo se utiliza para generar el query que obtiene un dataset de todos las aeronaves 
        que coincidan con el identificador de uno de los operadores.

        Parametros:
            operator_id -> int

        Ver en api.py:
            get_aircrafts(<arg>)
        
        Salida (string):
            query ej. "SELECT id_aeronave, tipo_aeronave, operador FROM aeronaves WHERE operador=..."
    '''
    return "SELECT id_aeronave, tipo_aeronave, operador FROM aeronaves WHERE operador="+operator_id+";"

def get_aircraft_id_query(aircraft, operator_id):
    '''
        Este metodo se utiliza para generar el query que obtiene el identificador unico de una aeronave 
        especifica por medio del tipo y el identificador de uno de los operadores.

        Parametros:
            aircraft -> string
            operator_id -> int

        Ver en api.py:
            get_aircraft_id(<arg>)
        
        Salida (string):
            query ej. "SELECT id_aeronave FROM aeronaves WHERE tipo_aeronave=..."
    '''
    return "SELECT id_aeronave FROM aeronaves WHERE tipo_aeronave='"+aircraft+"' And operador="+operator_id+";"

def get_operator_id_query(operator_name):
    '''
        Este metodo se utiliza para generar el query que obtiene el identificador unico de un 
        operador especifico por medio del nombre.

        Parametros:
            operator_name -> string

        Ver en api.py:
            get_operator_id(<arg>)
        
        Salida (int):
            query ej. SELECT id_operador FROM operadores WHERE nombre_operador=..."
    '''
    return "SELECT id_operador FROM operadores WHERE nombre_operador='"+operator_name+"';"

def get_specific_flight_query(day, month, year, department, operation_type, operator, aircraft):
    '''
        Este metodo se utiliza para generar el query que obtiene un dataset de un itinerario de vuelo 
        especifico basandose en el dia, mes, año de realizacion, departamento al que pertenece, 
        tipo de operacion, operador y tipo de aeronave.

        Parametros:
            day -> int
            month -> int
            year -> int 
            department -> string
            operation_type -> string
            operator -> string
            aircraft_type -> string

        Ver en api.py:
            get_specific_flight(<arg>)
        
        Salida (string):
            query ej. "SELECT TOP (1) * FROM itinerarios WHERE dia=..."
    '''
    return "SELECT TOP (1) * FROM itinerarios WHERE dia="+day+" And mes="+month+" And year="+year+" And departamento='"+department+"' And tipo_operacion='"+operation_type+"' And operador='"+operator+"' And tipo_aeronave='"+aircraft+"';"

def get_flight_personel_parameters_pxs_query(operation_type, aircraft):
    '''
        Este metodo se utiliza para generar el query que obtiene un dataset de los parametros de 
        personal establecidos para un tipo de vuelo especifico.

        Parametros:
            operation_type -> string
            aircraft_id -> int

        Ver en query_builder.py:
            get_flight_personel_parameters_pxs(<arg>)
        
        Salida (string):
            query ej. "SELECT * FROM parametros_personal_pxs WHERE tipo_operacion=..."
    '''
    return "SELECT * FROM parametros_personal_pxs WHERE tipo_operacion='"+operation_type+"' And aeronave='"+aircraft+"';"

def get_flight_personel_configuration_pxs_query(no_correlative):
    '''
        Este metodo se utiliza para generar el query que obtiene un dataset de la configuracion de 
        personal automatizada para un vuelo especifico.

        Parametros:
            no_correlative -> int

        Ver en api.py:
            get_flight_personel_configuration_pxs(<arg>)
        
        Salida (string):
            query ej. "SELECT * FROM configuracion_personal_vuelos_pxs WHERE no_correlativo=..."
    '''
    return "SELECT * FROM configuracion_personal_vuelos_pxs WHERE no_correlativo="+no_correlative+";"

def get_flight_et_personel_parameters_pxs_query(parameter_id):
    '''
        Este metodo se utiliza para generar el query que obtiene un dataset de los parametros 
        (banderas) de ET (estimated time) basados en el identificador de un parametro especifico 
        *relacionado a la tabla 'parametros_personal_pxs*.

        Parametros:
            parameter_id -> int

        Ver en api.py:
            get_flight_et_personel_parameters_pxs(<arg>)
        
        Salida (string):
            query ej. "SELECT * FROM et_parametros_personal_pxs WHERE id_parametro=..."
    '''
    return "SELECT * FROM et_parametros_personal_pxs WHERE id_parametro="+parameter_id+";"

def get_flight_times_personel_pxs_query(parameter_id):
    '''
        Este metodo se utiliza para generar un query que obtiene un dataset de los parametros de los 
        tiempos (minutos), antes o despues del tiempo estimado (ETA o ETD) en los que el personal 
        debe comenzar labores, basados en el identificador unico de un parametro especifico 
        *relacionado a la tabla 'parametros_personal_pxs*.

        Parametros:
            parameter_id -> int

        Ver en api.py:
            get_flight_times_personel_pxs(<arg>)
        
        Salida (string):
            query ej. "SELECT * FROM tiempos_personal_pxs WHERE id_parametro=..."
    '''
    return "SELECT * FROM tiempos_personal_pxs WHERE id_parametro="+parameter_id+";"

def get_configuracion_personal_pxs_query(no_correlative):
    '''
        Este metodo se utiliza para generar un query que obtiene un dataset de la configuracion de personal 
        para un itinerario de vuelo especifico basado en el numero de correlativo. 
        *relacionado a la tabla 'itinerarios*.

        Parametros:
            no_correlative -> int

        Ver en api.py:
            get_configuracion_personal_pxs_query(<arg>)
        
        Salida (string):
            query ej. "SELECT * FROM configuracion_personal_vuelos_pxs WHERE no_correlativo=..."
    '''
    return "SELECT * FROM configuracion_personal_vuelos_pxs WHERE no_correlativo="+no_correlative+";"