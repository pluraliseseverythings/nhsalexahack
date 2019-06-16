import os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from nhs_api import NHSOrganisationApi

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def launched():
    return question('Welcome to N. H. S. Hack Day. What would you like to know?')

@ask.intent("AMAZON.FallbackIntent")
def fallback():
    return statement("You can ask about the following things - car parking details, prescription costs, and A and E waiting times.")

@ask.intent("PrescriptionCosts")
def prescription_cost():
    return statement("The prescription charge in England is £9.00 per item.")

@ask.intent("WaitTimes")
def prescription_cost():
    return statement("There is a three and a half hour wait at your local A and E. This is below average for the time of year.")


@ask.intent("CarPark")
def car_park():
    client = NHSOrganisationApi()
    hospital_name = "Bristol eye hospital"
    hospital = client.get_hospital_by_name(hospital_name)
    if hospital == None:
        return statement("No hospital found with that name")

    facilities = client.get_hospital_facilities(hospital.id)
    if facilities.parking_summary:
        return statement(facilities.parking_summary)
    else:
        return statement("Sorry, there is no data for that hospital")

@ask.intent('RatingScore', convert={'hospital': str})
def rating_score(hospital):
    slot_value = getattr(hospital, 'value', None)
    resolutions = getattr(hospital, 'resolutions', None)

    if resolutions is not None:
        resolutions_per_authority = getattr(resolutions, 'resolutionsPerAuthority', None)
        if resolutions_per_authority is not None and len(resolutions_per_authority) > 0:
            values = resolutions_per_authority[0].get('values', None)
            if values is not None and len(values) > 0:
                value = values[0].get('value', None)
                if value is not None:
                    slot_value = value.get('name', slot_value)
    return statement('You asked about, ' + slot_value)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
