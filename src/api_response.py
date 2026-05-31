import json
from unittest.mock import Mock

import requests


def get_inf_through_api(
    address: str, filename: str
) -> str:  # "https://api.hh.ru/vacancies", 'data.json'
    """Получает инофрмацию с сайта и записывает в файл"""
    with open("../hh_vacancies.json") as f:
        hh_data = json.load(f)  # это уже объект Python

    mock_response = Mock()
    mock_response.json.return_value = hh_data
    mock_response.status_code = 200

    requests.get = Mock(return_value=mock_response)

    url = address
    params = {"area": 1}
    try:
        response = requests.get(url, params=params)
        result = response.json()

    except Exception as e:
        print(f"Непредвиденная ошибка при обработке запроса{e}")

    with open(filename, "w", encoding="utf-8") as f:
        try:
            json.dump(result, f, indent=4, ensure_ascii=False)
        except TypeError as e:
            print(f"ошибка {e}")

        return f"данные успешно считаны с сайта и записаны в файл {filename}"


if __name__ == "__main__":

    print(get_inf_through_api("https://api.hh.ru/vacancies", "data.json"))
