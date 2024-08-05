from flask import Flask, url_for, render_template,request
import sqlite3

import joblib
model = joblib.load('logistic_regression.lb')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('form.html')


@app.route("/prediction",methods=['GET','POST'])
def prediction():
    if  request.method == "POST":
        name = request.form["name"]
        age = int(request.form["age"])
        gender = int(request.form["gender"])
        flight_distance = int(request.form["flight_distance"])
        arrival_delay = int(request.form["arrival_delay"])
        departure_delay = int(request.form["departure_delay"])
        inflight_entertainment = int(request.form["inflight_entertainment"])
        baggage_handling = int(request.form["baggage_handling"])
        cleanliness = int(request.form["cleanliness"])
        customer_type = int(request.form["customer_type"])
        travel_type = int(request.form["travel_type"])
        flight_class = request.form["flight_class"]
        class_eco = 0
        class_eco_plus = 0
        if travel_type == 'ECO':
            class_eco = 1
        elif travel_type == 'ECO_PLUS':
            class_eco_plus = 1

        conn = sqlite3.connect("flight_user_data.db")
        conn.execute("""
                    insert into userrecord(
                        name, age, gender, flight_distance, arrival_delay, departure_delay, inflight_entertainment, 
                        baggage_handling, cleanliness, customer_type, travel_type, flight_class, class_eco, class_eco_plus)
                        values(?,?,?,?,?,?,?,?,?,?,?,?,?,?) """,
                        (name, age, gender, flight_distance, arrival_delay, departure_delay, inflight_entertainment, 
                        baggage_handling, cleanliness, customer_type, travel_type, flight_class, class_eco, class_eco_plus))

        conn.commit()
        conn.close()

        UNSEEN_DATA = [[age,
                        flight_distance,
                        inflight_entertainment,
                        baggage_handling,
                        cleanliness,
                        departure_delay,
                        arrival_delay,
                        gender,
                        customer_type,
                        travel_type,
                        class_eco,
                        class_eco_plus
                        ]]
        
        prediction = model.predict(UNSEEN_DATA)[0]
        print(prediction)
        labels = {'1':"SATISFIED",'0':"UNSATISFIED"}

        # return label[str(prediction)]
        return render_template('result.html',
                               output=labels[str(prediction)],
                               name=name,
                               age=age,
                               flight_distance=flight_distance,
                               inflight_entertainment=inflight_entertainment,
                               baggage_handling=baggage_handling,
                               cleanliness=cleanliness,
                               departure_delay=departure_delay,
                               arrival_delay=arrival_delay,
                               gender='Male' if gender == 1 else 'Female',
                               customer_type='Loyal' if customer_type == 0 else 'Disloyal',
                               flight_class=flight_class,
                               travel_type='Personal' if travel_type == 1 else 'Business'
                            )


if __name__ == "__main__" :
    app.run(debug=True)