"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

import pysnooper

app_history = []

app = Flask(__name__)


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
def between():
    """Returns the number of days between two dates"""
    add_to_history(request)

    data = request.get_json()
    if "first" not in data.keys() or "last" not in data.keys():
        return {"error": "Missing required data."}, 400
    try:
        first = convert_to_datetime(data["first"])
        last = convert_to_datetime(data["last"])
    except:
        return {"error": "Unable to convert value to datetime."}, 400

    return {"days": get_days_between(first, last)}


@app.route("/weekday", methods=["POST"])
def weekday():
    """Returns the day of the week a specific date is"""
    data = request.get_json()
    if "date" not in data.keys():
        return {"error": "Missing required data."}, 400
    try:
        week = convert_to_datetime(data["date"])
    except:
        return {"error": "Unable to convert value to datetime."}, 400
    return {"weekday": get_day_of_week_on(week)}


@app.route("/history", methods=["GET"])
@pysnooper.snoop()
def get_history():
    """Returns details on the last number of requests to the API"""
    data = request.args.to_dict()["number"]
    if not isinstance(data, int) or not 0 < int(data) <= 20:
        return {"error": "Number must be an integer between 1 and 20."}, 400


@app.route("/history", methods=["DELETE"])
def delete_history():
    """Deletes details of all previous requests to the API"""
    ...


@app.route("/current_age", methods=["GET"])
def current_age():
    """Returns a current age in years based on a given birthdate."""
    ...


if __name__ == "__main__":
    app.run(port=8080, debug=True)
