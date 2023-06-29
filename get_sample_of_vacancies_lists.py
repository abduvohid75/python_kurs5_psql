import json
import os

from class_vacancy import Vacancy
from classes_api import HeadHunterAPI #, SuperJobAPI


def get_sample_of_vacancies_list_hh_ru(search_query: str, keywords: str, top_vacancies: int):
    """
    Получение информаций о вакансиях из сайта ХедХантер согласно заданным фильтрам из схоранненого json файла и
    удаление промежуточного json файла
    """
    vacancies = []
    HeadHunterAPI().get_vacancies(search_query, keywords, top_vacancies)
    file_write_jobs = 'hh_jobs.json'
    try:
        with open(file_write_jobs) as json_file_read:
            content = json.load(json_file_read)
            json_file_read.close()
    except FileNotFoundError:

        return []

    else:
        vacancy_index = 0
        barrier = len(content)

        for vacancy in content:

            if vacancy["snippet"]["requirement"] is None:
                requirement = "Unknown"
            else:
                requirement = vacancy["snippet"]["requirement"]

            if vacancy["snippet"]["responsibility"] is None:
                responsibility = "Unknown"
            else:
                responsibility = vacancy["snippet"]["responsibility"]

            name = vacancy["name"]
            url = vacancy["alternate_url"]

            professional_roles = vacancy["professional_roles"][0]["name"]
            experience = vacancy["experience"]["name"]
            employment = vacancy["employment"]["name"]

            if vacancy["salary"] is None:
                salary_from = 0
                salary_to = 0

            else:

                if vacancy["salary"]["from"] is None:
                    salary_from = 0
                else:
                    salary_from = vacancy["salary"]["from"]

                if vacancy["salary"]["to"] is None:
                    salary_to = 0
                else:
                    salary_to = vacancy["salary"]["to"]

            vacancies.append(
                Vacancy(name, url, salary_from, salary_to, requirement, responsibility, professional_roles, experience,
                        employment))
            print(vacancy)

            vacancy_index += 1
            if vacancy_index == barrier:
                os.remove(file_write_jobs)
                break
        return vacancies

def unite_samples_of_vacancies(search_query: str, keywords: str, top_vacancies: int) -> object:
    """
    Получение данных о вакансиях и их объединение
    """
    vacancies_hh_ru = get_sample_of_vacancies_list_hh_ru(search_query, keywords, top_vacancies)
#    vacancies_sj_ru = get_sample_of_vacancies_list_sj_ru(search_query, keywords, top_vacancies)
#    vacancies_all = vacancies_sj_ru + vacancies_hh_ru
    vacancies_all = vacancies_hh_ru

    return vacancies_all
