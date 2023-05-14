import requests


def get_branches(city):
    url = "https://api.novaposhta.ua/v2.0/json/"
    params = {
        "apiKey": "e4e5c9f36feab441af0a7538ffe63b32",
        "modelName": "AddressGeneral",
        "calledMethod": "getWarehouses",
        "methodProperties": {"CityName": city},
    }
    # post request and get response
    response = requests.post(url, json=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data["data"]
    return []


def get_cities():
    url = "https://api.novaposhta.ua/v2.0/json/"
    params = {
        "apiKey": "e4e5c9f36feab441af0a7538ffe63b32",
        "modelName": "Address",
        "calledMethod": "getCities",
        "methodProperties": {},
    }
    response = requests.post(url, json=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            cities = [(city["Description"], city["Description"]) for city in data["data"]]
            return cities
    return []
