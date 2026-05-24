from unittest.mock import Mock
import requests
import json


with open ("../hh_vacancies.json") as f:
    hh_data = json.load(f) # это уже объект Python

mock_response = Mock()
mock_response.json.return_value = hh_data
mock_response.status_code = 200

requests.get = Mock(return_value=mock_response)


url = "https://api.hh.ru/vacancies"
params = {"area": 1}

response = requests.get(url, params=params)

result = response.json()

print(result)



