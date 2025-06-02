import requests
from typing import List, Dict
from src.abstract_api import VacancyAPI


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API HeadHunter"""

    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.__connected = False

    def connect(self) -> None:
        """Подключение к API hh.ru"""
        response = requests.get(self.BASE_URL)
        if response.status_code != 200:
            raise ConnectionError("Не удалось подключиться к hh.ru")
        self.__connected = True

    def get_vacancies(self, query: str, count: int = 100) -> List[Dict]:
        """Получение вакансий с hh.ru"""
        if not self.__connected:
            self.connect()

        params = {
            "text": query,
            "area": 113,  # Россия
            "per_page": count,
        }

        response = requests.get(self.BASE_URL, params=params)
        return response.json().get("items", [])