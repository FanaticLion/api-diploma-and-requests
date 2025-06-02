from abc import ABC, abstractmethod
from typing import List, Dict


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API платформ с вакансиями"""

    @abstractmethod
    def connect(self) -> None:
        """Подключение к API"""
        pass

    @abstractmethod
    def get_vacancies(self, query: str, count: int = 100) -> List[Dict]:
        """Получение вакансий по запросу"""
        pass