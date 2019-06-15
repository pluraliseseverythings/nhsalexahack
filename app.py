import os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, '/')


@app.route("/")
def hello():
    return "Hello from Python!"


@app.route("/alexa")
def alexa():
    return "Hello from Alexa!"


@ask.intent("PrescriptionCosts")
def prescription_cost():
    msg = render_template('It costs a million pounds')
    return statement(msg)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
