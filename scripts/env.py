'''
    @Author: Esteban Cabrera.
    @Version: 1.0.0.
    @See: app.py, query_builder.py.

    Este script contiene métodos creados para generar los queries a ejecutar en la base de datos
    para obtener la información deseada a base de parámetros establecidos.
'''

import scripts.env

'''
    Credenciales de la base de datos 'aatl' en Azure SQL Server:

    SERVER -> Referencia a la DNS del servidor de bases de datos mysqllaats.
    DATABASE -> Referencia a la base de datos 'aatl'.
    USERNAME -> Referencia al nombre de usuario del servidor.
    PASSWORD -> Referencia a la clave de usuario del servidor.
    DRIVER -> Referencia al nombre del DRIVER de base de datos requerido para la conexion y transacciones
              a realizar.
    PORT -> Referencia al puerto establecido en el servidor de bases de datos para permitir la conexion.
'''
SERVER = 'mysqllaats.database.windows.net'
DATABASE = 'aatl'
USERNAME = 'AdminLaats'
PASSWORD = 'Fn_1_5Laats' 
DRIVER = '{ODBC Driver 17 for SQL Server}' 
PORT = '1433'

'''
    Variables de ambiente para la gestion de sesion del usuario.

    USER_ID (int) -> Almacena temporalmente el identificador del usuario autenticado.
    DEPARTMENT (string) -> Almacena temporalmente el nombre del departamento al que pertenece el usuario.
    DEPARTMENT_COLOR (string) -> Almacena el color definido para el departamento al que pertenece 
    el usuario.
    LOGGED_IN (bool) -> Almacena una bandera True o False para determinar si un usuario esta autenticado.
'''
USER_ID = ''
DEPARTMENT = ''
DEPARTMENT_COLOR = ''
LOGGED_IN = False

'''
    Variable de ambiente que contiene los nombres de los agentes del departamento de PXS.

    Ver en app.py.
'''
PXS_PERSONEL_CONFIG = ['CREW CHIEF', 'AGENTES DE RAMPA', 'RAYOS X', 'MOSTRADOR', 'OPERADORES', 'FAJAS ENTRANDO']

def set_department_color():
    '''
        Este metodo se utiliza para asignarle el valor del color determinado para el departamento al que
        pertenece el usuario atenticado a la variable de ambiente DEPARTMENT_COLOR
    '''
    hex_color = '#ffffff'
    if DEPARTMENT == 'PXS':
        hex_color = '#8F99F7'
    elif DEPARTMENT == 'CGO':
        hex_color = '#EB7322'
    elif DEPARTMENT == 'SEC':
        hex_color = '#46B053'
    elif DEPARTMENT == 'TALLER':
        hex_color = '#2A7B80'
    elif DEPARTMENT == 'SAP':
        hex_color = '#7E2123'
    elif DEPARTMENT == 'PROYECTOS':
        hex_color = '#ffff00'
    elif DEPARTMENT == 'CALIDAD':
        hex_color = '#8EBD91'
    scripts.env.DEPARTMENT_COLOR = hex_color

