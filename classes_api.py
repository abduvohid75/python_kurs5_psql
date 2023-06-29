# coding: utf8
from class_json_saver import JSONSaver

import json
import os
import requests

from abc import ABC, abstractmethod


class SiteAPI(ABC):
    """
    Создание экземпляра класса для работы с API сайтов с вакансиями
    """

    @abstractmethod
    def get_vacancies(self, search_query: str, keywords: str, top_vacancies: int):
        pass


class HeadHunterAPI(SiteAPI):
    """
    Получение вакансий с разных платформ - с сайта HeadHunter

    """

    def get_vacancies(self, search_query: str, keywords: str, top_vacancies: int):
        hh_api = f'https://api.hh.ru/vacancies?text={search_query.replace(" ", "&")}&' \
                 f'description={keywords.replace(" ", "&")}&area=1&per_page=100'

        response = requests.get(hh_api, headers={"User-Agent": "K_ParserApp/1.0"})
        response_json = response.json()
        JSONSaver.save_vacancies_hh(response_json)  # Запись данных о вакансиях в файл hh_jobs
