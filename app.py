import re
from flask import Flask, render_template, request, redirect, url_for
import scripts.env
import scripts.data
from scripts.api import *
from scripts.data_handler import *

from datetime import datetime, date, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form["submit"]
        if form == "login":
            email = request.form["email"]
            pin = request.form["password"]
            auth = user_auth(email, pin)
            if auth:
                return redirect(url_for('dashboard'))
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
    if request.method == 'POST':
        req_date = request.form["date-selector"]
        year = req_date[0:4] 
        month = req_date[5:7] 
        day = req_date[8:10] 
        selected_flights = get_flights(day, month, year, 'PXS')
        return render_template('flights.html', flights=selected_flights)
    else:
        current_date = date.today() 
        year = current_date.strftime('%Y')
        month = current_date.strftime('%m')
        day = current_date.strftime('%d')
        selected_flights = get_flights(day, month, year, 'PXS')
        return render_template('flights.html', flights=selected_flights)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if scripts.env.LOGGED_IN:
        if request.method == 'POST':
            req_date = request.form["date-selector"]
            operator_id = request.form["operator-selector"]
            operation_type = request.form["operation-selector"]     
            aircraft_id = request.form["aircraft-selector"]       
            year = req_date[0:4] 
            month = req_date[5:7] 
            day = req_date[8:10] 
            min_time = req_date + 'T00:00:00'
            flights = get_flights(day, month, year, scripts.env.DEPARTMENT)
            flights_tags, flights_periods = get_flights_gantt_data(flights)
            operators = get_operators() 
            aircrafts = get_aircrafts(operator_id)

            operator_name = ''
            for operator in operators:
                if (operator[0] == int(operator_id)):
                    operator_name = operator[1]
            
            
            aircraft_type = ''
            for aircraft in aircrafts:
                if (aircraft[0] == int(aircraft_id)):
                    aircraft_type = aircraft[1]

            #
            flight = get_specific_flight(day, month, year, scripts.env.DEPARTMENT, operation_type, operator_name, aircraft_type)
            if len(flight) > 0:
                print(flight[0][0])
                no_correlative = str(flight[0][0])
                config = get_flight_personel_configuration_pxs(no_correlative)

                parameter = get_flight_personel_parameters_pxs(operation_type, aircraft_id)
                parameter_id = str(parameter[0][0])
                et_parameter = get_flight_et_personel_parameters_pxs(str(int(parameter_id)-1))

                start_time = flight[0][7]
                end_time = flight[0][8]
                
                times_parameter = get_flight_times_personel_pxs(parameter_id)
                print(times_parameter)
                print(et_parameter)
            #
            return render_template('dashboard.html',  department_color=scripts.env.DEPARTMENT_COLOR, department=scripts.env.DEPARTMENT, date=req_date, operators_list=operators, aircrafts_list=aircrafts, current_date=req_date, flights_tags=flights_tags, flights_periods=flights_periods, min_time=min_time, positions=scripts.data.positions, personel_times=scripts.data.personel_times)
        else:
            current_date = date.today()
            '''print(current_date)
            #min_time =     current_date + 'T00:00:00'
            flights = get_flights(day, month, year, scripts.env.DEPARTMENT)
            flights_tags, flights_periods = get_flights_gantt_data(flights)'''
            operators = get_operators()
            return render_template('dashboard.html',  department_color=scripts.env.DEPARTMENT_COLOR, operators_list=operators, current_date=current_date)#, flights_tags=flights_tags, flights_periods=flights_periods, min_time=min_time)
    else:
        return redirect(url_for('index'))

@app.route('/parameters')
def parameters():
    if scripts.env.LOGGED_IN:
        if scripts.env.DEPARTMENT == 'PXS':
            return render_template('parameters.html', department_color=scripts.env.DEPARTMENT_COLOR, personel_config = scripts.env.PXS_PERSONEL_CONFIG)
        return render_template('parameters.html', department_color=scripts.env.DEPARTMENT_COLOR, personel_config=[])
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True) 