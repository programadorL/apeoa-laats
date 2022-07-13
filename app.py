import re
from flask import Flask, render_template, request, redirect, url_for
import scripts.env
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

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if scripts.env.LOGGED_IN:
        if request.method == 'POST':
            req_date = request.form["date-selector"]
            operator = request.form["operator-selector"]
            flight_number = request.form["flight-selector"]
            year = req_date[0:4] 
            month = req_date[5:7] 
            day = req_date[8:10] 
            min_time = req_date + 'T00:00:00'
            flights = get_flights(day, month, year, scripts.env.DEPARTMENT)
            flights_tags, flights_periods = get_flights_gantt_data(flights)
            print(flights_tags, flights_periods )
            operators = get_operators() 
            return render_template('dashboard.html',  department_color=scripts.env.DEPARTMENT_COLOR, operators_list=operators, current_date=req_date, flights_tags=flights_tags, flights_periods=flights_periods, min_time=min_time)
        else:
            current_date = date.today()

            operators = get_operators()
            return render_template('dashboard.html',  department_color=scripts.env.DEPARTMENT_COLOR, operators_list=operators, current_date=current_date)
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