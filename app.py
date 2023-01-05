'''
    @Author: Esteban Cabrera.
    @Version: 1.0.0.
    @See: Flask framework.
    @See: /scripts/env.py
    @See: /scripts/data_handler.py
    @See: /scripts/pfm.py

    @Relevant: https://flask.palletsprojects.com/en/2.2.x/

    Este script contiene métodos creados para enrutar las pantallas de la App y enviarles los parametros
    necesarios para renderizar la data necesaria en cada una de ellas. Importa las librerias necesarias
    para el funcionamiento del sistema y contiene la inicializacion del framework Flask.
'''

from flask import Flask, render_template, request, redirect, url_for
import scripts.env
from scripts.api import *
from scripts.data_handler import *
from scripts.pfm import *

from datetime import datetime, date, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    '''
        Este metodo se utiliza para enrutar la aplicacion a la pagina index del proyecto (login). 

        Ver en /templates/:
            index.html
        
        Salida (html):
            index.html
    '''
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    '''
        Este metodo se utiliza para enrutar la aplicacion a la pagina index del proyecto (login). 

        Ver en /templates/:
            index.html
        
        Salida (html):
            index.html
    '''
    if request.method == 'POST':
        form = request.form["submit"]
        if form == "login":
            email = request.form["email"]
            pin = request.form["password"]
            auth = user_auth(email, pin)
            if auth:
                return redirect(url_for('flights'))
            else:
                return str(auth)
        elif form == "reset":
            email = request.form["email"]
            old_pin = request.form["old-password"]
            new_pin = request.form["new-password"]
            new_pin2 = request.form["new-password2"]
            reset = pin_reset(email, old_pin, new_pin, new_pin2)
            if reset:
                return render_template("index.html")
            else:
                return str(reset)
    return False

@app.route('/fligths', methods=['GET', 'POST'])
def flights():
    '''
        Este metodo se utiliza para enrutar la aplicacion a la pagina (flights.html) de los vuelos diarios 
        (posterior a la autenticacionn del usuario). Carga por default los valores de la fecha actual para 
        obtener un dataset con los vuelos que coincidan con la fecha y el departamento al que el usuario 
        pertenece.
        En el caso que exista una peticion POST, se recopilan los datos que el usuario ha establecido para la
        filtracion de los vuelos en el elemento 'filter-section' del archivo /templates/dashboard.html y se 
        obtiene un nuevo dataset de vuelos.
        Tambien se toman en cuenta las variables de ambiente establecidas para la configuracion
        de color definido para el departamento al que pertenece el usuario. 
        Adicionalmente, se hace un llamado a un metodo que genera dos datasets que contienen la informacion
        necesaria para renderizar un diagrama de gantt con los vuelos del dia especificado.

        Ver en /templates/:
            flights.html
        
        Ver en /scripts/env.py
            DEPARTMENT_COLOR
            DEPARTMENT
        
        Ver en /scripts/api.py
            get_flights(<args>)

        Ver en /scripts/data_handler.py
            get_flights_gantt_data(<args>)
        
        Salida:
            flights.html -> html
            scripts.env.DEPARTMENT_COLOR -> string 
            scripts.env.DEPARTMENT -> string
            req_date -> string
            selected_flights -> Array
            flights_tags -> Array
            flights_periods -> Array 
            min_time -> string
    '''
    if request.method == 'POST':
        req_date = request.form["date-selector"]
        year = req_date[0:4] 
        month = req_date[5:7] 
        day = req_date[8:10] 
        min_time = req_date + 'T00:00:00'
        selected_flights = get_flights(day, month, year, 'PXS')
        flights_tags, flights_periods = get_flights_gantt_data(selected_flights)
        return render_template('flights.html', department_color=scripts.env.DEPARTMENT_COLOR, department=scripts.env.DEPARTMENT, date=req_date, flights=selected_flights, flights_tags=flights_tags, flights_periods=flights_periods, min_time=min_time)
    else:
        current_date = date.today() 
        year = current_date.strftime('%Y')
        month = current_date.strftime('%m')
        day = current_date.strftime('%d')
        min_time = year + '-' + month + '' + day + 'T00:00:00'
        selected_flights = get_flights(day, month, year, 'PXS')
        flights_tags, flights_periods = get_flights_gantt_data(selected_flights)
        return render_template('flights.html', department_color=scripts.env.DEPARTMENT_COLOR, department=scripts.env.DEPARTMENT, date=current_date, flights=selected_flights, flights_tags=flights_tags, flights_periods=flights_periods, min_time=min_time)

@app.route('/process_flight_data/<no_correlative>', methods=['GET', 'POST'])
def set_flight_data(no_correlative):
    return redirect(url_for('dashboard', no_correlative=no_correlative))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    '''
        Este metodo se utiliza para enrutar la aplicacion a la pagina (dashboard.html) de los vuelos diarios 
        (posterior a la autenticacionn del usuario). Carga por default los valores de la fecha actual para 
        obtener un dataset con los vuelos que coincidan con la fecha y el departamento al que el usuario 
        pertenece.
        En el caso que exista una peticion POST, se recopilan los datos que el usuario ha establecido para la
        filtracion de los vuelos en el elemento 'filter-section' del archivo /templates/dashboard.html y se 
        obtiene un nuevo dataset.
        Tambien se toman en cuenta las variables de ambiente establecidas para la configuracion
        de color definido para el departamento al que pertenece el usuario. 
        Adicionalmente, se hace un llamado a un metodo que genera dos datasets que contienen la informacion
        necesaria para renderizar un diagrama de gantt con los vuelos del dia especificado.

        Ver en /templates/:
            dashboard.html
        
        Ver en /scripts/env.py
            DEPARTMENT_COLOR
            DEPARTMENT
        
        Ver en /scripts/api.py
            get_flights(<args>)

        Ver en /scripts/data_handler.py
            get_flights_gantt_data(<args>)
        
        Salida:
            dashboard.html -> html
            scripts.env.DEPARTMENT_COLOR -> string
            scripts.env.DEPARTMENT -> string
            flight_info -> Array
            req_date -> string
            flights_tags -> Array
            flights_periods -> Array
            min_time -> string
            agents -> Array
            tiempos -> Array
            staff_config -> Array
            matrix_freq -> Array
            matrix_titles -> Array
            titles -> Array
            countNumb -> int
            start_time -> string
            end_time -> string
            time_titles -> Array
            freq -> Array
            asig -> Array
            disp -> Array
            hours -> Array
    '''
    if scripts.env.LOGGED_IN:
        args = request.args
        no_correlative = args.get("no_correlative")

        flight = get_flight_by_correlative(no_correlative)

        aircraft_type = flight[0][14]
        operator_name = flight[0][10]
        
        operator_id = get_operator_id(operator_name)
        operator_id = str(operator_id[0][0])

        aircraft_id = get_aircraft_id(aircraft_type, operator_id)

        aircraft_id = str(aircraft_id[0][0])

        operation_type = flight[0][11]
        
        year = str(flight[0][1])
        if flight[0][3] < 10:
            month = '0' + str(flight[0][3])
        else:
            month = str(flight[0][3])
        if flight[0][2] < 10:   
            day = '0' + str(flight[0][2])
        else:
            day = str(flight[0][2])

        req_date = year + '-' + month + '-' +  day 

        min_time = req_date + 'T00:00:00'

        flights = get_flights(day, month, year, scripts.env.DEPARTMENT)
        flights_tags, flights_periods = get_flights_gantt_data(flights)

        start_time = (flight[0][2]- 1)*24*4
        end_time = (flight[0][2])*24*4
        print(start_time, end_time)

        flight_info = flight[0]

        staff_config = get_configuracion_personal_pxs(no_correlative)

        tiempos, agents, matrix_freq, time_titles = create_pfm(int(no_correlative), int(flight[0][3]))

        asig_per = matrix_freq[7]
        req_per = matrix_freq[8]
        titles = True
        countNumb = 0

        freq = matrix_freq[9][start_time:end_time]
        asig = matrix_freq[7][start_time:end_time]
        disp = matrix_freq[8][start_time:end_time]
        hours = time_titles[1:]

        matrix_titles = ['Crew chiefs', 'Operadores', 'Agentes de Rampa', 'Agentes de mostrador', 'Agentes de fajas', 'Agentes de rayos x', 'Agentes de limpieza', 'Personal asignado', 'Personal disponible', 'Diff. Personal']
        return render_template('dashboard.html', department_color=scripts.env.DEPARTMENT_COLOR, department=scripts.env.DEPARTMENT, flight_info=flight_info, date=req_date, current_date=req_date, flights_tags=flights_tags, flights_periods=flights_periods, min_time=min_time, positions=agents, personel_times=tiempos, staff_config=staff_config, matrix_freq=matrix_freq, matrix_titles=matrix_titles, titles=titles, countNumb=countNumb, start_time=start_time, end_time=end_time, time_titles=time_titles, freq=freq, asig=asig, disp=disp, hours=hours)
    else:
        return redirect(url_for('index'))

@app.route('/parameters')
def parameters():
    '''
        Este metodo se utiliza para enrutar la aplicacion a la pagina (parameters.html) en la cual se
        realizan los cambios manuales de la configuracion del personal para un vuelo en especifico.

        Ver en /templates/:
            dashboard.html
        
        Ver en /scripts/env.py
            DEPARTMENT_COLOR
            DEPARTMENT
        
        Salida:
            parameters.html -> html
    '''
    if scripts.env.LOGGED_IN:
        if scripts.env.DEPARTMENT == 'PXS':
            return render_template('parameters.html', department_color=scripts.env.DEPARTMENT_COLOR, personel_config = scripts.env.PXS_PERSONEL_CONFIG)
        return render_template('parameters.html', department_color=scripts.env.DEPARTMENT_COLOR, personel_config=[])
    else:
        return redirect(url_for('index'))

'''
    Inicializacion de la aplicacion.

    *                                                                                                        *
        app.run() tiene como parametro debug=True. Este debe quitarse al momento de poner el proyecto en
        produccion, ya que al tenerlo activado, los errores de ejecucion se veran reflejados en consola o en
        el navegador.
    *                                                                                                        *
'''
if __name__ == "__main__":
    app.run(debug=True)     