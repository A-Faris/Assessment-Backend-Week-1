"""Tests for the API routes"""

# pylint: skip-file

from unittest.mock import patch
from datetime import datetime

import pytest


class TestBetween:
    """Tests for the between route"""

    def test_disallows_get_requests(self, test_app):
        """Checks that GET requests are not permitted."""

        result = test_app.get("/between")

        assert result.status_code == 405

    @pytest.mark.parametrize("data", ({},
                                      {"first": 1},
                                      {"second": 2},
                                      {"first": 1, "econd": 2},
                                      {"A": 1, "B": 2}))
    def test_requires_data(self, data, test_app):
        """Checks that the route rejects missing data."""

        result = test_app.post("/between", json=data)

        assert result.status_code == 400
        assert result.json == {
            "error": "Missing required data."
        }

    @pytest.mark.parametrize("data", ({"first": 1, "last": 2},
                                      {"first": 33.0, "last": True},
                                      {"first": "red", "last": "blue"},
                                      {"first": "23/1/1999", "last": "1999/2/16"}))
    def test_requires_valid_data(self, data, test_app):
        """Checks that the route rejects invalid data."""

        result = test_app.post("/between", json=data)

        assert result.status_code == 400
        assert result.json == {
            "error": "Unable to convert value to datetime."
        }

    @patch("app.add_to_history")
    def test_calls_add_to_history(self, fake_add, test_app):
        """Checks that the route calls the add_to_history function."""

        test_app.post("/between", json={
            "first": "12.1.2000", "last": "14.1.2000"
        })

        assert fake_add.called
        assert fake_add.call_count == 1

    @patch("app.convert_to_datetime")
    def test_calls_convert(self, fake_convert, test_app):
        """Checks that the route calls the conversion function."""

        test_app.post("/between", json={
            "first": "12.1.2000", "last": "14.1.2000"
        })

        assert fake_convert.called
        assert fake_convert.call_count == 2

    @patch("app.get_days_between")
    def test_calls_between(self, fake_between, test_app):
        """Checks that the route calls the get_days_between function."""

        test_app.post("/between", json={
            "first": "12.1.2000", "last": "14.1.2000"
        })

        assert fake_between.called
        assert fake_between.call_count == 1

    @pytest.mark.parametrize("data, out", (({"first": "12.1.2000", "last": "14.1.2000"}, 2),
                                           ({"first": "1.1.2000",
                                            "last": "1.2.2000"}, 31),
                                           ({"first": "12.2.2001",
                                            "last": "12.2.2002"}, 365),
                                           ({"first": "1.2.2000",
                                            "last": "31.1.2000"}, -1),
                                           ({"first": "1.1.2000",
                                            "last": "1.1.2000"}, 0),
                                           ({"first": "28.2.2000",
                                            "last": "1.3.2000"}, 2),
                                           ({"first": "1.1.2000",
                                            "last": "7.1.2000"}, 6),
                                           ({"first": "12.1.2002",
                                            "last": "14.1.2001"}, -363),
                                           ))
    def test_returns_correct_value(self, data, out, test_app):
        """Checks that the route returns accurate responses."""

        result = test_app.post("/between", json=data)

        assert result.status_code == 200
        assert result.json == {
            "days": out
        }


class TestWeekday:
    """Tests for the weekday route"""

    def test_disallows_get_requests(self, test_app):
        """Checks that GET requests are not permitted."""

        result = test_app.get("/weekday")

        assert result.status_code == 405

    @patch("app.convert_to_datetime")
    def test_calls_convert(self, fake_convert, test_app):
        """Checks that the route calls the conversion function."""

        test_app.post("/weekday", json={
            "date": "12.1.2000"
        })

        assert fake_convert.called
        assert fake_convert.call_count == 1

    @patch("app.get_day_of_week_on")
    def test_calls_day_of_week(self, fake_get_day, test_app):
        """Checks that the route calls the get_day_of_week_on function."""

        test_app.post("/weekday", json={
            "date": "12.1.2000"
        })

        assert fake_get_day.called
        assert fake_get_day.call_count == 1

    @pytest.mark.parametrize("data", ({},
                                      {"first": 1},
                                      {"dat": 2},
                                      {"Date": 3},
                                      {"dates": 4}))
    def test_requires_data(self, data, test_app):
        """Checks that the route rejects missing data."""

        result = test_app.post("/weekday", json=data)

        assert result.status_code == 400
        assert result.json == {
            "error": "Missing required data."
        }

    @pytest.mark.parametrize("data", ({"date": 1},
                                      {"date": "1880.12.01"},
                                      {"date": "red"},
                                      {"date": "24.5.19"},
                                      {"date": "24/5/1999"}))
    def test_requires_valid_data(self, data, test_app):
        """Checks that the route rejects invalid data."""

        result = test_app.post("/weekday", json=data)

        assert result.status_code == 400
        assert result.json == {
            "error": "Unable to convert value to datetime."
        }

    @pytest.mark.parametrize("data, out", (({"date": "09.10.2023"}, "Monday"),
                                           ({"date": "10.10.2023"}, "Tuesday"),
                                           ({"date": "11.10.2023"}, "Wednesday"),
                                           ({"date": "12.10.2023"}, "Thursday"),
                                           ({"date": "13.10.2023"}, "Friday"),
                                           ({"date": "14.10.2023"}, "Saturday"),
                                           ({"date": "15.10.2023"}, "Sunday")
                                           ))
    def test_returns_correct_value(self, data, out, test_app):
        """Checks that the route returns accurate responses."""

        result = test_app.post("/weekday", json=data)

        assert result.status_code == 200
        assert result.json == {
            "weekday": out
        }

    @patch("app.add_to_history")
    def test_calls_add_to_history(self, fake_add, test_app):
        """Checks that the route calls the add_to_history function."""

        test_app.post("/between", json={
            "first": "12.1.2000", "last": "14.1.2000"
        })

        assert fake_add.called
        assert fake_add.call_count == 1


class TestHistory:
    """Tests for the history route"""

    def test_disallows_post_requests(self, test_app):
        """Checks that POST requests are not permitted."""

        result = test_app.post("/history")

        assert result.status_code == 405

    @pytest.mark.parametrize("n", (("red"),
                                   (13.5),
                                   (0),
                                   (24),
                                   (-8)))
    def test_rejects_invalid_parameter(self, n, test_app):
        """Checks that invalid number parameters are rejected."""

        result = test_app.get(f"/history?number={n}")

        assert result.status_code == 400
        assert result.json == {
            "error": "Number must be an integer between 1 and 20."
        }

    @pytest.mark.parametrize("n", (1, 2, 3, 4, 10))
    def test_returns_correct_number_of_records(self, n, test_app):
        """Checks that the number parameter is respected."""

        # Seed with excess data
        for _ in range(2 * n):
            test_app.get("/history")

        result = test_app.get(f"/history?number={n}")

        assert result.status_code == 200
        assert len(result.json) == n

    def test_number_defaults_to_five(self, test_app):
        """Checks that 5 history items are returned if no number is specified."""

        # Seed history
        for _ in range(10):
            test_app.get("/history")

        result = test_app.get("/history")

        assert result.status_code == 200
        assert len(result.json) == 5

    def test_clears_history_on_delete(self, test_app):
        """Checks that a DELETE request is handled appropriately."""

        # Seed history
        for _ in range(10):
            test_app.get("/history")

        # Clear it
        result = test_app.delete("/history")

        # Check that clearing happened without error
        assert result.status_code == 200
        assert result.json == {
            "status": "History cleared"
        }

    def test_restarts_history_after_delete(self, test_app):
        """Checks that history is reset after a DELETE request."""

        # Seed history
        for _ in range(10):
            test_app.get("/history")

        # Clear it
        result = test_app.delete("/history")

        # Check it's empty (except for this latests history call)
        result = test_app.get("/history")
        data = result.json

        assert result.status_code == 200
        assert len(data) == 1
        assert data == [
            {"at": datetime.now().strftime("%d/%m/%Y %H:%M"),
             "method": "GET",
             "route": "history"}
        ]

    def test_history_returns_in_reverse_order(self, test_app):
        """Tests that the history route returns the most recent calls."""

        for _ in range(3):
            test_app.get("/history")

        test_app.post("/weekday", json={"date": "09.10.2023"})

        result = test_app.get("/history")
        data = result.json
        methods = [x["method"] for x in data]

        assert methods == ["GET", "POST", "GET", "GET", "GET"]

    def test_history_tracks_between(self, test_app):
        """Checks that the between route adds to the history"""

        test_app.post("/between", json={"first": "12.1.2000", "last": "14.1.2000"})

        result = test_app.get("/history")
        data = result.json

        assert data[1]["method"] == "POST"
        assert data[1]["route"] == "between"

    def test_history_tracks_weekday(self, test_app):
        """Checks that the weekday route adds to the history"""

        test_app.post("/weekday", json={"date": "09.10.2023"})

        result = test_app.get("/history")
        data = result.json

        assert data[1]["method"] == "POST"
        assert data[1]["route"] == "weekday"

    @patch("app.add_to_history")
    def test_calls_add_to_history(self, fake_add, test_app):
        """Checks that the route calls the add_to_history function."""

        test_app.post("/between", json={
            "first": "12.1.2000", "last": "14.1.2000"
        })

        assert fake_add.called
        assert fake_add.call_count == 1

    def test_history_records_history_before_returning(self, test_app):
        """Checks that the weekday route adds to the history"""

        test_app.get("/history")
        test_app.get("/history")
        result = test_app.get("/history")
        data = result.json

        assert len(data) == 3
        assert all(x["route"] == "history" for x in data)


class TestCurrentAge:
    """Tests for the current_age route"""

    def test_disallows_post_requests(self, test_app):
        """Checks that GET requests are not permitted."""

        result = test_app.post("/current_age")

        assert result.status_code == 405

    def test_requires_date_param(sef, test_app):
        """Checks that a date param is required."""

        result = test_app.get(f"/current_age")

        assert result.status_code == 400
        assert result.json == {
                "error": "Date parameter is required."
        }

    @pytest.mark.parametrize("birthdate", ('birthdate', 0, '23/01/2000', '19-02-02', '3rd of March 1827'))
    def test_rejects_invalid_input(self, birthdate, test_app):
        """Checks that invalid date values are rejected."""

        result = test_app.get(f"/current_age?date={birthdate}")

        assert result.status_code == 400
        assert result.json == {
            "error": "Value for data parameter is invalid."
        }

    @pytest.mark.parametrize("birthdate", ('2027-03-03', '3000-02-28', '1901-12-22', '0001-01-01', '1097-01-27'))
    @patch("app.get_current_age")
    def test_returns_on_valid_input(self, fake_get_current_age, birthdate, test_app):
        """Checks that valid date values call appropriate functions and return expected result."""

        fake_get_current_age.return_value = 0
    
        print(birthdate)
        result = test_app.get(f"/current_age?date={birthdate}")

        assert result.status_code == 200
        assert "current_age" in result.json
        assert result.json["current_age"] == 0
