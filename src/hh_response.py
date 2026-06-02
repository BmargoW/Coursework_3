from unittest.mock import Mock
import requests
import json
import psycopg2


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
result_list = result['items']


list_id_vacancy = [(element['id'],)for element in result_list]
list_title_vacancy = [(element['name'],) for element in result_list]
list_id_employeer = [(element['employer']['id'],) for element in result_list]
list_salary = [(element['salary']['from'],)for element in result_list]
list_requirement = [(element['snippet']['requirement'],) for element in result_list]
list_link_vacancy = [(element['alternate_url'],) for element in result_list]
list_company = [(element['employer']['name'],) for element in result_list]

employeer_data = []
for i in result_list:
    emp_id = i['employer']['id']
    emp_name = i['employer']['name']
    employeer_data.append((emp_id, emp_name))


conn = psycopg2.connect(
    host="localhost",
    database="test-1",
    user="postgres",
    password="6162"
)


with conn.cursor() as cur:
    cur.execute("CREATE TABLE employer(personal_id int PRIMARY KEY, company_name varchar(50))")# домашняя работа
    cur.execute("CREATE TABLE vacancy (vacancy_id int PRIMARY KEY, vacancy_title varchar(50), employee_id int REFERENCES employer(personal_id))")

conn.commit()
conn.close()

with conn.cursor() as cur:
    cur.execute("ALTER TABLE vacancy ADD COLUMN salary int")# домашняя работа
    cur.execute("ALTER TABLE vacancy ADD COLUMN requirement text")
    cur.execute("ALTER TABLE vacancy ADD COLUMN linc_vacancy text")

conn.commit()
conn.close()



with conn.cursor() as cur:

    cur.executemany("INSERT INTO employer (personal_id, company_name) VALUES (%s, %s) ON CONFLICT DO NOTHING", employeer_data)

    for i in range(len(list_id_vacancy)):
        cur.execute("""
            INSERT INTO vacancy (vacancy_id, vacancy_title, employee_id, salary, requirement, linc_vacancy)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (list_id_vacancy[i][0], list_title_vacancy[i][0], list_id_employeer[i][0],
             list_salary[i][0], list_requirement[i][0], list_link_vacancy[i][0])
        )



conn.commit()
conn.close()
