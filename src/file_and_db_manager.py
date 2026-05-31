import json

import psycopg2

from config import config


def greate_db(name_db: str):  # test2
    """создает базу данных"""
    params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"CREATE DATABASE {name_db}")
        print(f"База данных {name_db} успешно создана!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        cur.close()
        conn.close()


def creating_tables_in_bd(name_db: str):  # test3
    """Создает таблицы в базе данных"""

    params = config()
    conn = psycopg2.connect(database=name_db, **params)

    with conn.cursor() as cur:
        try:
            cur.execute(
                "CREATE TABLE employer(personal_id int PRIMARY KEY, company_name varchar(50))"
            )
            cur.execute(
                "CREATE TABLE vacancy (vacancy_id int PRIMARY KEY, vacancy_title varchar(50), \
            employee_id int REFERENCES employer(personal_id),salary int, requirement text, linc_vacancy text)"
            )
            print(f"Таблицы в базе данных {name_db} успешно созданы!")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            conn.commit()
            conn.close()


def filling_table(filename: str, name_db: str):  # 'data.json', test2
    """Заполняет данными таблицы  базы данных"""
    with open(filename) as f:
        data = json.load(f)

    result_list = data["items"]

    list_id_vacancy = [(element["id"],) for element in result_list]
    list_title_vacancy = [(element["name"],) for element in result_list]
    list_id_employeer = [(element["employer"]["id"],) for element in result_list]
    list_salary = [(element["salary"]["from"],) for element in result_list]
    list_requirement = [(element["snippet"]["requirement"],) for element in result_list]
    list_link_vacancy = [(element["alternate_url"],) for element in result_list]

    employeer_data = []
    for i in result_list:
        emp_id = i["employer"]["id"]
        emp_name = i["employer"]["name"]
        employeer_data.append((emp_id, emp_name))

    params = config()
    conn = psycopg2.connect(database=name_db, **params)

    with conn.cursor() as cur:
        try:
            cur.executemany(
                "INSERT INTO employer (personal_id, company_name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                employeer_data,
            )

            for i in range(len(list_id_vacancy)):
                cur.execute(
                    """
                    INSERT INTO vacancy (vacancy_id, vacancy_title, employee_id, salary, requirement, linc_vacancy)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (
                        list_id_vacancy[i][0],
                        list_title_vacancy[i][0],
                        list_id_employeer[i][0],
                        list_salary[i][0],
                        list_requirement[i][0],
                        list_link_vacancy[i][0],
                    ),
                )
            print(f"Таблицы в базе данных {name_db} успешно заполнены!")

        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            conn.commit()
            conn.close()


if __name__ == "__main__":
    greate_db("test3")
    creating_tables_in_bd("test3")
    filling_table("data.json", "test3")
