import psycopg2
from config import config
from src.DBConnection import DBConnection
from src.hh_API import HeadHunterAPI


class DBManager(DBConnection, HeadHunterAPI):
    """Класс для работы с базой данных"""

    def __init__(self):
        super().__init__()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with psycopg2.connect(dbname=self.db_name, **config()) as conn:
            with conn.cursor() as cur:
                query = "SELECT company_name, open_vacancies FROM companies ORDER BY open_vacancies"
                cur.execute(query)
                rows = cur.fetchall()
                # тут же пока что и распечатываем
                for row in rows:
                    print("Название компании:", row[0])  # company_name
                    print("Количество вакансий:", row[1])  # open_vacancies
                    print("-" * 40)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию"""
        with psycopg2.connect(dbname=self.db_name, **config()) as conn:
            with conn.cursor() as cur:
                query = ("SELECT  v.vacancy_name, c.company_name, v.salary_min, v.salary_max, v.url FROM vacancies v "
                         "JOIN companies c ON v.company_id = c.id;")
                cur.execute(query)
                rows = cur.fetchall()
                return rows

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        with psycopg2.connect(dbname=self.db_name, **config()) as conn:
            with conn.cursor() as cur:
                # считаем среднюю заработную плату по всем вакансиям
                query_salary = "SELECT avg((salary_min + salary_max) / 2) FROM vacancies"
                cur.execute(query_salary)
                rows = cur.fetchone()

                # делаем переменную для вывода количества вакансий по которым идет расчёт
                query_count = """
                SELECT COUNT(v.id) FROM vacancies v JOIN companies c ON v.company_id = c.id WHERE c.open_vacancies > 0
                """
                cur.execute(query_count)
                row_count = cur.fetchone()
                return print(f"Средняя зарплата по {row_count[0]} вакансиям", round(rows[0], 2))

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with psycopg2.connect(dbname=self.db_name, **config()) as conn:
            with conn.cursor() as cur:
                query = ("select vacancy_name from vacancies where ((salary_min + salary_max) / 2)"
                         " > (select avg((salary_min + salary_max) / 2) from vacancies)")
                cur.execute(query)
                rows = cur.fetchall()
                return rows

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        with psycopg2.connect(dbname=self.db_name, **config()) as conn:
            with conn.cursor() as cur:
                # vacancy_name в нижнем регистре
                # поиск вхождений вводимого слова %{keyword}%'
                query = (f"SELECT vacancy_name, salary_min, salary_max, url FROM vacancies WHERE lower(vacancy_name) "
                         f"like '%{keyword}%'")
                cur.execute(query)
                rows = cur.fetchall()
                return rows
