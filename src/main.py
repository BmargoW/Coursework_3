from src.api_response import get_inf_through_api
from src.file_and_db_manager import greate_db, creating_tables_in_bd, filling_table
from src.db_manager import DBManager


def user_interaction():
    print(
        "Добро пожаловать в программу обработки инофрмации, полученной с сайта, сохранения данной \
информации в базе данных и предоставлением инструментов для работы с базой данных Для этого Вам необходимо:"
    )

    address = input(
        "Введите URL, по которому Вы хотите найти инофрмацию"
    )  # "https://api.hh.ru/vacancies"
    filename = input(
        "Введите название файла, в который будет сохранятся информация"
    )  # "data.json"
    name_db = input("Введите название Вашей будущей базы данных")  # "test3"

    get_inf_through_api(address, filename)
    greate_db(name_db)
    creating_tables_in_bd(name_db)
    filling_table(filename, name_db)

    launch = DBManager()

    choice = (
        input(
            str("Введите 'yes', если хотите получить список всех компаний и количество\
вакансий у каждой компании из БД или 'no'")
        )
        .strip()
        .lower()
    )
    if choice == "yes":
        print(launch.get_companies_and_vacancies_count(name_db))
    elif choice == "no":
        print("Пропуск операции")
    else:
        print("Ошибка: Пожалуйста, введите именно 'yes' или 'no'.")

    choice_2 = (
        input(
            str("Введите 'yes', если хотите получить список всех вакансий с указанием \
названия компании из БД или 'no'")
        )
        .strip()
        .lower()
    )
    if choice_2 == "yes":
        print(launch.get_all_vacancies(name_db))
    elif choice_2 == "no":
        print("Пропуск операции")
    else:
        print("Ошибка: Пожалуйста, введите именно 'yes' или 'no'.")

    choice_3 = (
        input(
            str(
                "Введите 'yes', если хотите получить среднюю зарплату по вакансиям из БД или 'no'"
            )
        )
        .strip()
        .lower()
    )
    if choice_3 == "yes":
        print(launch.get_avg_salary(name_db))
    elif choice_3 == "no":
        print("Пропуск операции")
    else:
        print("Ошибка: Пожалуйста, введите именно 'yes' или 'no'.")

    choice_4 = input(str("Введите 'yes', если хотите получить список всех вакансий, \
у которых зарплата выше средней по всем вакансиям из БД или 'no'")).strip().lower()
    if choice_4 == "yes":
        print(launch.get_vacancies_with_higher_salary(name_db))
    elif choice_4 == "no":
        print("Пропуск операции")
    else:
        print("Ошибка: Пожалуйста, введите именно 'yes' или 'no'.")


if __name__ == "__main__":

    user_interaction()
