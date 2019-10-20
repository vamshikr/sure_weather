import os

import pytest
import requests
from http import HTTPStatus


class TestSureWeather:

    URL = "http://localhost:8080/current_weather"

    def test_valid_latlon_valid_services0(self):
        response = requests.get(self.URL, params={"latitude":33.33, "longitude":44.44})
        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert "latitude" in data and data["latitude"] == 33.33
        assert "longitude" in data and data["longitude"] == 44.44
        assert 'temperature' in data and "fahrenheit" in data["temperature"] \
               and "celsius" in data["temperature"]

    def test_valid_latlon_valid_services3(self):

        response = requests.get(self.URL,
                                params={"latitude":33.33, "longitude":44.44,
                                        "services":["accuweather", "noaa", "weather.com"]})
        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert "latitude" in data and data["latitude"] == 33.33
        assert "longitude" in data and data["longitude"] == 44.44
        assert 'temperature' in data and "fahrenheit" in data["temperature"] \
               and "celsius" in data["temperature"]

    def test_valid_latlon_valid_services2(self):

        response = requests.get(self.URL,
                                params={"latitude":33.33, "longitude":44.44,
                                        "services":["accuweather", "noaa"]})
        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert "latitude" in data and data["latitude"] == 33.33
        assert "longitude" in data and data["longitude"] == 44.44
        assert 'temperature' in data and "fahrenheit" in data["temperature"] \
               and "celsius" in data["temperature"]

    def test_valid_latlon_valid_services1(self):

        response = requests.get(self.URL,
                                params={"latitude":33.33, "longitude":44.44,
                                        "services":["accuweather"]})
        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert "latitude" in data and data["latitude"] == 33.33
        assert "longitude" in data and data["longitude"] == 44.44
        assert 'temperature' in data and "fahrenheit" in data["temperature"] \
               and "celsius" in data["temperature"]

    def test_valid_latlon_invalid_services(self):

        response = requests.get(self.URL,
                                params={"latitude":33.33, "longitude":44.44,
                                        "services":["acccuweatherr"]})
        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        data = response.json()
        assert "error_code" in data and data["error_code"] == "INVALID_INPUT"


    def test_invalid_latlon1(self):

        response = requests.get(self.URL,
                                params={"latitude": 200.33, "longitude":44.44})
        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        data = response.json()
        assert "error_code" in data and data["error_code"] == "INVALID_INPUT"

        response = requests.get(self.URL,
                                params={"latitude": 33.33, "longitude":344.44})
        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        data = response.json()
        assert "error_code" in data and data["error_code"] == "INVALID_INPUT"

        response = requests.get(self.URL,
                                params={"latitude": 333.33, "longitude":344.44})
        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        data = response.json()
        assert "error_code" in data and data["error_code"] == "INVALID_INPUT"

    @pytest.mark.skipif('GOOGLE_MAPS_APIKEY' not in os.environ,
                        reason="""works only if GOOGLE_MAPS_APIKEY is defined in 
                        web application environment""")
    def test_valid_zipcode(self):

        response = requests.get(self.URL, params={"zipcode": 78728})

        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert "latitude" in data and "longitude" in data
        assert 'temperature' in data and "fahrenheit" in data["temperature"] \
               and "celsius" in data["temperature"]

        response = requests.get(self.URL, params={"zipcode": 7728})

        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert "latitude" in data and "longitude" in data
        assert 'temperature' in data and "fahrenheit" in data["temperature"] \
               and "celsius" in data["temperature"]

    @pytest.mark.skipif('GOOGLE_MAPS_APIKEY' not in os.environ,
                        reason="""works only if GOOGLE_MAPS_APIKEY is defined in 
                        web application environment""")
    def test_invalid_zipcode(self):

        response = requests.get(self.URL, params={"zipcode": 769080728})

        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        data = response.json()
        assert "error_code" in data and data["error_code"] == "INVALID_INPUT"

