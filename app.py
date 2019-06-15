import os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from nhs_api import NHSOrganisationApi

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def launched():
    return question('Welcome to N. H. S. Hack Day.')

@ask.intent("PrescriptionCosts")
def prescription_cost():
    return statement("The prescription charge in England is £9.00 per item.")

@ask.intent("CarPark")
def car_park():
    client = NHSOrganisationApi()
    hospital_name = "Bristol eye hospital"
    hospital = client.get_hospital_by_name(hospital_name)
    facilities = client.get_hospital_facilities(hospital.id)
    if facilities.parking_summary:
        return statement(facilities.parking_summary)
    else:
        return statement("Sorry, there is no data for that hospital")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
