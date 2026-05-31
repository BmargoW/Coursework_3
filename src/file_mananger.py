import json
import psycopg2
from config import config


with open ('data.json') as f:
    data = json.load(f)

result_list = data['items']

# def creating_tables_in_bd():
#
#     params = config()
#     conn = psycopg2.connect(
#                 **params
#             )
#
#     with conn.cursor() as cur:
#         cur.execute("CREATE TABLE employer(personal_id int PRIMARY KEY, company_name varchar(50))")# домашняя работа
#         cur.execute("CREATE TABLE vacancy (vacancy_id int PRIMARY KEY, vacancy_title varchar(50), \
#         employee_id int REFERENCES employer(personal_id),salary int, requirement text, linc_vacancy text)")
#
#     conn.commit()
#     conn.close()


#def
# list_id_vacancy = [(element['id'],)for element in result_list]
# list_title_vacancy = [(element['name'],) for element in result_list]
# list_id_employeer = [(element['employer']['id'],) for element in result_list]
# list_salary = [(element['salary']['from'],)for element in result_list]
# list_requirement = [(element['snippet']['requirement'],) for element in result_list]
# list_link_vacancy = [(element['alternate_url'],) for element in result_list]
# list_company = [(element['employer']['name'],) for element in result_list]
#
# employeer_data = []
# for i in result_list:
#     emp_id = i['employer']['id']
#     emp_name = i['employer']['name']
#     employeer_data.append((emp_id, emp_name))
#
#
#
# with conn.cursor() as cur:
#
#     cur.executemany("INSERT INTO employer (personal_id, company_name) VALUES (%s, %s) ON CONFLICT DO NOTHING", employeer_data)
#
#     for i in range(len(list_id_vacancy)):
#         cur.execute("""
#             INSERT INTO vacancy (vacancy_id, vacancy_title, employee_id, salary, requirement, linc_vacancy)
#             VALUES (%s, %s, %s, %s, %s, %s)""",
#             (list_id_vacancy[i][0], list_title_vacancy[i][0], list_id_employeer[i][0],
#              list_salary[i][0], list_requirement[i][0], list_link_vacancy[i][0])
#         )
#
# conn.commit()
# conn.close()