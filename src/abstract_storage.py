from abc import ABC, abstractmethod
from typing import List
from .vacancy import Vacancy


class Storage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию"""
        pass

    @abstractmethod
    def get_vacancies(self, **filters) -> List[Vacancy]:
        """Получить вакансии по фильтрам"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию"""
        pass
