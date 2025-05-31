from abc import ABC, abstractmethod
from typing import List, Dict


class VacancyAPI(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Подключение к API"""
        pass

    @abstractmethod
    def get_vacancies(self, query: str, count: int = 100) -> List[Dict]:
        """Получение вакансий"""
        pass
