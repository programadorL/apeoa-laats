from flask import Flask, render_template, request, redirect, url_for
import scripts.env
from scripts.api import *

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
            time = request.form["time-selector"]
            operator = request.form["operator-selector"]
            flight_number = request.form["flight-selector"]
            
            operators = get_operators()
            return render_template('dashboard.html',  department_color=scripts.env.DEPARTMENT_COLOR, operators_list=operators)
        else:
            current_date = date.today()

            operators = get_operators()
            return render_template('dashboard.html',  department_color=scripts.env.DEPARTMENT_COLOR, operators_list=operators, current_date=current_date)
    else:
        return redirect(url_for('index'))

@app.route('/parameters')
def parameters():
    if scripts.env.LOGGED_IN:
        return render_template('parameters.html', department_color=scripts.env.DEPARTMENT_COLOR)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)