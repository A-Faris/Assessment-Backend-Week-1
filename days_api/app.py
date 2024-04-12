"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

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
    except ValueError:
        return {"error": "Unable to convert value to datetime."}, 400

    return {"days": get_days_between(first, last)}


@app.route("/weekday", methods=["POST"])
def weekday():
    """Returns the day of the week a specific date is"""
    add_to_history(request)

    data = request.get_json()
    if "date" not in data.keys():
        return {"error": "Missing required data."}, 400
    try:
        week = convert_to_datetime(data["date"])
    except ValueError:
        return {"error": "Unable to convert value to datetime."}, 400
    return {"weekday": get_day_of_week_on(week)}, 200


@app.route("/history", methods=["GET"])
def history():
    """Returns details on the last number of requests to the API"""
    add_to_history(request)

    args = request.args.to_dict()
    number = args.get("number", "5")

    if not number.isdigit():
        return {"error": "Number must be an integer between 1 and 20."}, 400

    number = int(number)
    if not 1 <= number <= 20:
        return {"error": "Number must be an integer between 1 and 20."}, 400

    return app_history[::-1][:number], 200


@app.route("/history", methods=["DELETE"])
def delete_history():
    """Deletes details of all previous requests to the API"""
    app_history.clear()
    return {"status": "History cleared"}, 200


@app.route("/current_age", methods=["GET"])
def current_age():
    """Returns a current age in years based on a given birthdate."""
    add_to_history(request)

    args = request.args.to_dict()
    birthdate = args.get("date")

    if not birthdate and not isinstance(birthdate, date):
        return {"error": "Date parameter is required."}, 400

    try:
        return {"current_age": get_current_age(birthdate)}
    except TypeError:
        return {"error": "Value for data parameter is invalid."}, 400


if __name__ == "__main__":
    app.run(port=8080, debug=True)
