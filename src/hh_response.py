
import json

import psycopg2

from config import config


def read_vacancies_from_file(path="../hh_vacancies.json"):
    """Читает вакансии из сохранённого JSON-файла.
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)["items"]


def save_to_db(vacancies):
    """Записывает работодателей и вакансии в БД напрямую."""
    conn = psycopg2.connect(**config())

    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employer (
                    personal_id int PRIMARY KEY,
                    company_name varchar(50)
                )""")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancy (
                    vacancy_id int PRIMARY KEY,
                    vacancy_title varchar(50),
                    employee_id int REFERENCES employer(personal_id),
                    salary int,
                    requirement text,
                    link_vacancy text
                )""")

            employers = []
            vacancies_rows = []
            for v in vacancies:
                employers.append((v["employer"]["id"], v["employer"]["name"]))
                # зарплаты у вакансии может не быть — подстраховываемся
                salary = (v.get("salary") or {}).get("from")
                requirement = (v.get("snippet") or {}).get("requirement")
                vacancies_rows.append((
                    v["id"], v["name"], v["employer"]["id"],
                    salary, requirement, v["alternate_url"],
                ))

            cur.executemany(
                "INSERT INTO employer (personal_id, company_name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                employers,
            )
            cur.executemany(
                """INSERT INTO vacancy (vacancy_id, vacancy_title, employee_id, salary, requirement, link_vacancy)
                   VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                vacancies_rows,
            )


if __name__ == "__main__":
    data = read_vacancies_from_file()
    save_to_db(data)
    print(f"Загружено вакансий: {len(data)}")