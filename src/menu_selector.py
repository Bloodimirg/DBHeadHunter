from src.DBManager import DBManager


class MenuSelector(DBManager):
    """Класс управления меню"""

    def __init__(self):
        super().__init__()
        self.previous_choices = []

    def display_menu(self):
        print("Меню:")
        print("1. Отобразить все компании и количество их вакансий")
        print("2. Отобразить общую информацию")
        print("3. Отобразить среднюю заработную плату")
        print("4. Отобразить список всех вакансий, заработная плата которых выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Завершить сеанс")

    def select_option(self):
        while True:
            self.display_menu()
            choice = input("Выберите действие: ")
            if choice.isdigit():
                choice = int(choice)
                if 0 <= choice <= 5:
                    if choice == 0 and len(self.previous_choices) > 0:
                        return self.previous_choices.pop()
                    else:
                        self.previous_choices.append(choice)
                        return choice
                else:
                    print("Некорректный выбор. Пожалуйста, выберите существующий пункт из меню.")
            else:
                print("Пожалуйста, введите число.")

    def start_menu(self):
        """Функция выбора методов в зависимости от ввода пользователя"""
        while True:

            db_select = DBManager()
            menu = MenuSelector()
            user_select_menu = menu.select_option()

            if user_select_menu == 1:
                db_select.get_companies_and_vacancies_count()

            elif user_select_menu == 2:
                all_vacancies = db_select.get_all_vacancies()
                for vacancy in all_vacancies:
                    vacancy_name = vacancy[0]
                    company_name = vacancy[1]
                    min_salary = vacancy[2] if vacancy[2] is not None else "Не указано"
                    max_salary = vacancy[3] if vacancy[3] is not None else "Не указано"
                    url_vacancy = vacancy[4]
                    print(f"Вакансия: {vacancy_name}"
                          f"\nКомпания: {company_name}"
                          f"\nЗарплата от: {min_salary}"
                          f"\nЗарплата до: {max_salary}"
                          f"\nСсылка на вакансию: {url_vacancy}"
                          f"\n{'-' * 40}")

            elif user_select_menu == 3:
                db_select.get_avg_salary()

            elif user_select_menu == 4:
                print(f"Вакансии с наибольшей средней заработной платой:\n{'-' * 40}")
                higher_salary = db_select.get_vacancies_with_higher_salary()
                for vacancy in higher_salary:
                    print(f"{vacancy[0]} - {vacancy[1]}")

            elif user_select_menu == 5:
                user_input = input("Введите ключевое слово в названии вакансии, например 'python'\n").lower()
                search_vacancies = db_select.get_vacancies_with_keyword(user_input)
                edited_vacancies = [vacancies[0:] for vacancies in search_vacancies]
                for vacancy in edited_vacancies:
                    min_salary = vacancy[1] if vacancy[1] is not None else "Не указано"
                    max_salary = vacancy[2] if vacancy[2] is not None else "Не указано"
                    print(
                        f"Вакансия: {vacancy[0]} \nЗарплата от: {min_salary} \nЗарплата до: {max_salary} \nСсылка: {vacancy[3]}")
                    print('😎' * 10)

            elif user_select_menu == 0:
                exit()
