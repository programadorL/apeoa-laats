import scripts.env

SERVER = 'mysqllaats.database.windows.net'
DATABASE = 'aatl'
USERNAME = 'AdminLaats'
PASSWORD = 'Fn_1_5Laats' 
DRIVER = '{ODBC Driver 17 for SQL Server}' 
PORT = '1433'

USER_ID = ''
DEPARTMENT = ''

DEPARTMENT_COLOR = ''

LOGGED_IN = False

PXS_PERSONEL_CONFIG = ['CREW CHIEF', 'AGENTES DE RAMPA', 'RAYOS X', 'MOSTRADOR', 'OPERADORES', 'FAJAS ENTRANDO']

def set_department_color():
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

