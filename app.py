import os
from flask import Flask
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, '/')


@app.route("/")
def hello():
    return "Hello from Python!"


@app.route("/alexa")
def alexa():
    return "Hello from Alexa!"


@ask.intent("PrescriptionCost")
def prescription_cost():
    return statement("response to prescription cost")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
