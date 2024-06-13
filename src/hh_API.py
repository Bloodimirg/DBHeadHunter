import requests
from config import hh_api_config


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.url = "https://api.hh.ru"
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = dict(page=0, per_page=100, employer_id=hh_api_config.get('employer_ids'), only_with_salary=True)

    def get_employers_data(self) -> list[dict]:
        """Получение информации о работодателях"""
        employers_info = []
        for ids in self.params['employer_id']:

            url = self.url + '/employers/' + ids
            response = requests.get(url, headers=self.headers, params=self.params)

            if response.status_code == 200:
                company_data = response.json()

                company_id = company_data.get('id')
                company_name = company_data.get('name')
                city = company_data.get('area', {}).get('name')
                url = company_data.get('alternate_url')
                employer_info = {
                    'id': company_id,
                    'name': company_name,
                    'city': city,
                    'url': url,
                }
                employers_info.append(employer_info)

            else:
                print(f"Ошибка в ID компании {ids}")

        return employers_info

    def get_vacancies_data(self) -> list:
        """Получение деталей по всем вакансиям всех работодателей"""
        vacancies = []
        url = self.url + '/vacancies'

        while self.params['page'] != 20:
            response = requests.get(url, headers=self.headers, params=self.params)
            data = response.json()
            vacancies.extend(data['items'])
            self.params['page'] += 1
        return vacancies
