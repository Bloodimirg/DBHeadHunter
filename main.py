from src.DBConnection import DBConnection
from src.hh_API import HeadHunterAPI
from src.menu_selector import MenuSelector


def main():
    db_manager = DBConnection()
    hh_parser = HeadHunterAPI()

    db_manager.create_database()  # создаем базу данных
    db_manager.create_tables()  # создаем таблицы

    employers = hh_parser.get_employers_data()  # информация о компаниях
    vacancies = hh_parser.get_vacancies_data()  # информация о вакансиях компаний

    db_manager.truncate_tables()  # очищаем таблицы
    db_manager.insert_employers(employers)  # заполняем таблицу с работодателями
    db_manager.insert_vacancies(vacancies)  # заполняем таблицу с вакансиями

    menu_selector = MenuSelector()
    menu_selector.start_menu()  # запускаем селектор меню


if __name__ == '__main__':
    main()
