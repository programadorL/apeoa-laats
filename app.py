from flask import Flask, render_template
import os

directory_path = os.getcwd()

app = Flask(__name__) #static_folder = directory_path)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)