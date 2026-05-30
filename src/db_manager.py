
from abc import ABC, abstractmethod
import psycopg2
from config import config



class BDContact(ABC):

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    # def flight_data(self):
    #     pass

class DatabaseSelection(BDContact):
    """Конструктор для подключения к БД"""

    def __init__(self):
        params = config()
        self.conn = psycopg2.connect(
            **params
        )


    def get_companies_and_vacancies_count(self)->str:
        """Получает список всех компаний и количество вакансий у каждой компании из БД."""
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                " SELECT employer.company_name, COUNT(*) FROM employer  \
                  INNER JOIN vacancy ON employer.personal_id = vacancy.employee_id\
                  GROUP BY employer.company_name")
            rows = cur.fetchall()

        conn.commit()
        conn.close()
        finding = ""
        for i in rows:
            finding += f"Наименование компании: {i[0]}, количество вакансий:{i[1]} \n"
        return finding

    def get_all_vacancies(self) -> str:
        """Получает список всех вакансий с указанием названия компании из БД."""
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                " SELECT vacancy.vacancy_title || ' ' || employer.company_name AS vacancies, vacancy.salary,\
                 vacancy.linc_vacancy FROM vacancy\
                 JOIN employer ON vacancy.employee_id = employer.personal_id")
            rows = cur.fetchall()

        conn.commit()
        conn.close()
        finding = ""
        for i in rows:
            finding += f"Вакансия с названием компании: {i[0]}, зарплата:{i[1]} руб, \
            ссылка на вакансию: {i[2]} \n"
        return finding

    def get_avg_salary(self) -> str:
        """Получает среднюю зарплату по вакансиям из БД."""
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                " SELECT AVG (salary) FROM vacancy")
            rows = cur.fetchone()

        conn.commit()
        conn.close()

        finding = f"Величина средней зарплаты по вакансиям: {round(rows[0],2)} рублей"
        return finding

    def get_vacancies_with_higher_salary(self) -> str:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям из БД."""
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                " SELECT vacancy_title, salary FROM vacancy\
                 WHERE salary > (SELECT AVG (salary) FROM vacancy)")
            rows = cur.fetchall()

        conn.commit()
        conn.close()
        finding = ""
        for i in rows:
            finding += f" Наименование вакансии, уровень зарплаты по которой\
 выше среднего: {i[0]}, зарплата:{i[1]} руб \n"
        return finding

    def get_vacancies_with_keyword(self, criteria: str) -> str:
        """Выводит из БД информацию в консоль о вакансиях по указанному пользователем ключевому слову."""
        conn = self.conn
        with conn.cursor() as cur:
            search_pattern = f'%{criteria}%'
            query = "SELECT * FROM vacancy WHERE vacancy_title LIKE %s"
            cur.execute(query, (search_pattern,))
            rows = cur.fetchall()

        conn.commit()
        conn.close()
        finding = ""
        for i in rows:
            finding += f" Наименование вакансии, с указанным ключевым словом: {i[1]},\
зарплата:{i[3]} рублей, требования: {i[4]}, cсылка на вакансию: {i[5]}\n, "
        return finding

if __name__ == "__main__":
    launch = DatabaseSelection()

    #companies_and_vacancies = launch.get_companies_and_vacancies_count()
    #all_vacancies = launch.get_all_vacancies()
    #avg_salary = launch.get_avg_salary()
    #higher_salary = launch.get_vacancies_with_higher_salary()
    #selected_vacancy = launch.get_vacancies_with_keyword("Python")
    #print(selected_vacancy)