import os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from nhs_api import NHSOrganisationApi
from flask import request
import json, urllib.request


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
def wait_time():
    content = request.get_json()
    # print(content)
    # datastore = json.loads(content)
    name = content['request']['intent']['slots']['waithospital']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    with urllib.request.urlopen("https://ae-waits.herokuapp.com") as url:
        data = json.loads(url.read().decode())
        for items in data:
            items['hosp_simp']=items['hospital'].split(' (')[0]
            if name in items['hosp_simp']:
                if items['is_open']=='false':
                    return statement('This hospital is closed')
                else:
                    return statement('There are currently '+items['current_patients']+' patients waiting at '+name)


@ask.intent("CarPark")
def car_park():
    content = request.get_json()
    # print(content)
    # datastore = json.loads(content)
    ods = content['request']['intent']['slots']['hospital']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']

    client = NHSOrganisationApi()
    hospital = client.get_hospital_by_ods_code(ods)
    if hospital == None:
        return statement("Sorry, no hospital found with the ods code %s" % ods)

    facilities = client.get_hospital_facilities(hospital.id)
    alexa_response = f"{hospital.title}"
    if facilities.parking == True:
        alexa_response += f" has parking facilities. "
    elif facilities.parking == False:
        alexa_response += f" does not have parking facilities. "

    # Sometimes there will be extra information
    if facilities.parking_summary:
        alexa_response += facilities.parking_summary

    return statement(alexa_response)

@ask.intent('RatingScore')
def rating_score():
    content = request.get_json()
    # print(content)
    # datastore = json.loads(content)
    ods = content['request']['intent']['slots']['hospital']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']

    client = NHSOrganisationApi()
    hospital = client.get_hospital_by_ods_code(ods)
    if hospital == None:
        return statement(f"Sorry, no hospital found with code {ods}")

    return statement(f"{hospital.title} is rated {round(hospital.star_rating, 1)} out of 5 stars")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
