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
                     '4934'],    # Билайн
    'vacancies_per_page': 100,
    'area': 113,
    'only_with_salary': True
}


def config(filename='database.ini'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section('postgresql'):  # Удалено использование параметра section
        params = parser.items('postgresql')  # Также удалено использование параметра section
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section postgresql is not found in the database.ini file')
    return db

