def get_user_auth_query(email, password):
    return "SELECT usuario, pin, id_usuario FROM usuarios WHERE usuario ='" + email + "' And pin ='" + password + "';"

def get_pin_reset_query(email, new_pin):
    return "UPDATE usuarios SET pin='" + new_pin + "' WHERE usuario='" + email + "';"

def get_flights_query(day, month, year, department):
    return "SELECT dia, mes, year, origen, destino, hora_ingreso, hora_egreso, no_vuelo, operador, no_correlativo, tipo_aeronave FROM itinerarios WHERE dia='"+day+"' And  mes='"+month+"' And  year='"+year+"' And departamento='"+department+"' And tipo_operacion <> 'RECEPCION' and tipo_aeronave <> '';"

def get_flight_by_correlative_query(no_correlative):
    return "SELECT * FROM itinerarios WHERE no_correlativo="+no_correlative+";"

def get_department_query(user_id):
    return "SELECT departamento FROM Personal_General WHERE codigo_empleado="+str(user_id)+";"  

def get_operators_query():
    return "SELECT id_operador, nombre_operador FROM operadores WHERE id_operador > 1 ORDER BY nombre_operador ASC;"

def get_aircrafts_query(operator_id):
    return "SELECT id_aeronave, tipo_aeronave, operador FROM aeronaves WHERE operador="+operator_id+";"

def get_aircraft_id_query(aircraft, operator_id):
    return "SELECT id_aeronave FROM aeronaves WHERE tipo_aeronave='"+aircraft+"' And operador="+operator_id+";"

def get_operator_id_query(operator_name):
    return "SELECT id_operador FROM operadores WHERE nombre_operador='"+operator_name+"';"

def get_flights_query2(operator_id):
    return "SELECT no_vuelo FROM vuelos WHERE operador='"+operator_id+"' ORDER BY no_vuelo ASC;"

def get_specific_flight_query(day, month, year, department, operation_type, operator, aircraft):
    return "SELECT TOP (1) * FROM itinerarios WHERE dia="+day+" And mes="+month+" And year="+year+" And departamento='"+department+"' And tipo_operacion='"+operation_type+"' And operador='"+operator+"' And tipo_aeronave='"+aircraft+"';"

def get_flight_personel_parameters_pxs_query(operation_type, aircraft):
    return "SELECT * FROM parametros_personal_pxs WHERE tipo_operacion='"+operation_type+"' And aeronave='"+aircraft+"';"

def get_flight_personel_configuration_pxs_query(no_correlative):
    return "SELECT * FROM configuracion_personal_vuelos_pxs WHERE no_correlativo="+no_correlative+";"

def get_flight_et_personel_parameters_pxs_query(parameter_id):
    return "SELECT * FROM et_parametros_personal_pxs WHERE id_parametro="+parameter_id+";"

def get_flight_times_personel_pxs_query(parameter_id):
    return "SELECT * FROM tiempos_personal_pxs WHERE id_parametro="+parameter_id+";"

def get_configuracion_personal_pxs_query(no_correlative):
    return "SELECT * FROM configuracion_personal_vuelos_pxs WHERE no_correlativo="+no_correlative+";"