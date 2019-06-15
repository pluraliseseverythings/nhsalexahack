import os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, '/')


@app.route("/")
def hello():
    return statement("You have opened the skill.")

@app.route("/alexa")
def alexa():
    return "Hello from Alexa!"


@ask.intent("PrescriptionCosts")
def prescription_cost():
    return statement("The prescription charge in England is £9.00 per item.")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
