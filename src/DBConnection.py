import psycopg2
from config import config


class DBConnection:
    """Класс подключения базы данных"""

    def __init__(self):
        params = config()
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()
        self.db_name = 'head_hunter'
        self.conn.autocommit = True

    def conn_close(self):
        self.conn.close()

    def create_database(self):
        """Создаем базу данных"""
        try:
            self.cur.execute(f"""CREATE DATABASE {self.db_name};""")
        except Exception as e:
            print(f"Error creating database: {e}")
        finally:
            self.conn.close()

    def create_tables(self):
        """Создаем две таблицы с компаниями и их вакансиями"""
        with psycopg2.connect(dbname=self.db_name, **config()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS companies(
                id INT PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                city VARCHAR(255),
                url VARCHAR(255),
                open_vacancies INT
                )""")

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies(
                id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                company_id INT NOT NULL REFERENCES companies(id),
                salary_min INT,
                salary_max INT)""")

    def insert_employers(self, employer_data):
        """Заполняем таблицу работодателей"""
        with psycopg2.connect(dbname=self.db_name, **config()) as conn:
            with conn.cursor() as cursor:
                for employer in employer_data:
                    cursor.execute("""
                    INSERT INTO companies(id, company_name, city, url, open_vacancies) VALUES (%s, %s, %s, %s, %s);
                    
                    """, (
                        employer['id'],
                        employer['name'],
                        employer['city'],
                        employer['url'],
                        employer['open_vacancies']
                    ))

    def insert_vacancies(self, vacancies_data):
        """Заполняем таблицу вакансиями работодателей"""
        with psycopg2.connect(dbname=self.db_name, **config()) as conn:
            with conn.cursor() as cursor:
                for vacancies in vacancies_data:
                    cursor.execute("""
                    INSERT INTO vacancies(id, vacancy_name, url, company_id, salary_min, salary_max) VALUES (%s, %s, %s, %s, %s, %s);
        
                    """, (
                        vacancies['id'],
                        vacancies['name'],
                        vacancies['alternate_url'],
                        vacancies['employer']['id'],
                        vacancies['salary']['from'],
                        vacancies['salary']['to']
                    ))

    def truncate_tables(self):
        """Очищаем таблицы перед заполнением"""
        with psycopg2.connect(dbname=self.db_name, **config()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """TRUNCATE TABLE companies RESTART IDENTITY CASCADE;"""
                )
                cursor.execute(
                    """TRUNCATE TABLE vacancies RESTART IDENTITY CASCADE;"""
                )
