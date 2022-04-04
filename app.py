from flask import Flask, render_template, request
from scripts.api import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        pin = request.form["password"]
        auth = user_auth(email, pin)
    return str(auth)
        

if __name__ == "__main__":
    app.run(debug=True)