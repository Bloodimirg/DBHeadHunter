from configparser import ConfigParser

hh_api_config = {
    'employer_ids': ['4767781',  # AlfaBit
                     '2944864',  # OOO AVPOWER
                     '1671874',  # Media 108
                     '3492171',  # Сорэкс
                     '2544353',  # Инспектор Клауд
                     '9244855',  # CRTEX
                     '1723062',  # DIGINETICA
                     '9322264',  # Налитек
                     '3642645',  # aQsi
                     '1740'],  # яндекс
    'vacancies_per_page': 100,
    'area': 113,
    'only_with_salary': True
}


def config(section='postgresql', filename='database.ini'):
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        params = parser.items(section)
        db = dict(params)
        return db
    else:
        raise Exception(f'Section {section} is not found in the {filename}')

