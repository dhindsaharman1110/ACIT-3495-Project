from flask import Flask, redirect, render_template, request
from itsdangerous import json
import requests
from connexion import NoContent
import json
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/readings', methods=['POST'])
def handle_data():
    print(request.form)
    myobj = {}
    myobj['user_fname'] = request.form['first_name']
    myobj['user_lname'] = request.form['last_name']
    myobj['user_email'] = request.form['email']
    myobj['user_phone'] = request.form['phone']
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
        return redirect("http://127.0.0.1:8080/result")
    #    request.post("http://127.0.0.1:8080/result)"


@app.route('/about')
def about():
    return render_template('about.html')

values=[]
@app.route('/result',  methods=['POST','GET'])
def result():
    if request.method == 'POST':
        print(request.method)
        #request.method == 'POST':
        myobj={}
        print("------------")
        print(type(request.json))
        json_data = json.loads(request.json)
        print(type(json_data))
        #print(json_data['max_height'])
        if len(values) != 0:
            values[0]=json_data 
        else:
            values.append(json_data)
        print("FINALLY------------------->")
        print(values[0]['user_BMR'] )
        return render_template('result.html', max_bmr_male=str(json_data['max_bmr_male']))
    
    else:
        return render_template('result.html',
                max_bmr_male=values[0]['max_bmr_male'],
                max_bmr_female=values[0]['max_bmr_female'],
                min_bmr_male=values[0]['min_bmr_male'],
                min_bmr_female=values[0]['min_bmr_female'],
                avg_bmr_male=values[0]['avg_bmr_male'],
                avg_bmr_female=values[0]['avg_bmr_female'],
                user_BMR=values[0]['user_BMR']
                )
    

#@app.route('/result', methods=['GET'])
#def proof():
#    r=request.post("http://127.0.0.1:8090/readings")

if __name__ == "__main__":
    app.run(port=8080)
