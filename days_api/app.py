"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

import pysnooper

app_history = []

app = Flask(__name__)


@app.route("/history", methods=["GET", "DELETE"])
def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({"message": "Welcome to the Days API."})


@app.route("/between", methods=["POST"])
@pysnooper.snoop()
def between():
    data = request.get_json()
    if "first" not in data.keys() or "last" not in data.keys():
        return {"error": "Missing required data."}, 400

    first = data["first"]
    last = data["last"]
    if isinstance(first, datetime) or isinstance(last, datetime):
        return get_days_between(first, last)
    return {"error": "Unable to convert value to datetime."}, 400


@app.route("/weekday", methods=["POST"])
def weekday():
    ...


@app.route("/current_age", methods=["GET"])
def current_age():
    ...


if __name__ == "__main__":
    app.run(port=8080, debug=True)
