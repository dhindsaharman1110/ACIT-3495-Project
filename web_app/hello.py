from flask import Flask, redirect, render_template, request
from itsdangerous import json
import requests
from connexion import NoContent
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/readings', methods=['POST'])
def handle_data():
    print(type(request.form['first_name']))
    myobj = {}
    myobj['user_fname'] = request.form['first_name']
    myobj['user_lname'] = request.form['last_name']
    myobj['user_age'] = request.form['age']
    if request.form['gender'] == "1":
        myobj['user_gender'] = "Female"
    elif request.form['gender'] == "2":
        myobj['user_gender'] = "Male"
    myobj['user_height'] = request.form['height']
    myobj['user_weight'] = request.form['weight']
    print(myobj)

    r=requests.post("http://127.0.0.1:8090/readings", json=myobj)
    # return user_fname, user_lname, user_age, user_gender, user_height, user_weight
    if r.status_code == 200:
        return redirect("http://127.0.0.1:8080/")
    
@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

if __name__ == "__main__":
    app.run(port=8080)