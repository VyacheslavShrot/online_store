import requests


def get_european_countries():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)

    if response.status_code == 200:
        countries_data = response.json()
        european_countries = [(country["name"]["common"], country["name"]["common"]) for country in countries_data if
                              country["region"] == "Europe" and country["name"]["common"] not in ["Ukraine", "Russia"]]
        return european_countries

    return []
