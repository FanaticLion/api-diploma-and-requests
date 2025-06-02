from dataclasses import dataclass
from typing import List, Dict


@dataclass(order=False)
class Vacancy:
    """Класс для представления вакансии с возможностью сравнения по зарплате"""
    __slots__ = ['_title', '_url', '_salary_from', '_salary_to', '_description', '_requirements']

    def __init__(self, title: str, url: str,
                 salary_from: int = 0, salary_to: int = 0,
                 description: str = "", requirements: str = ""):
        self._title = title
        self._url = url
        self._salary_from = salary_from
        self._salary_to = salary_to
        self._description = description
        self._requirements = requirements
        self._validate_data()

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary_from(self) -> int:
        return self._salary_from

    @property
    def salary_to(self) -> int:
        return self._salary_to

    @property
    def description(self) -> str:
        return self._description

    @property
    def requirements(self) -> str:
        return self._requirements

    def _validate_data(self):
        """Приватный метод валидации данных"""
        if not isinstance(self._title, str) or not self._title:
            raise ValueError("Название вакансии должно быть непустой строкой")
        if not isinstance(self._url, str) or not self._url.startswith("http"):
            raise ValueError("URL должен быть валидной ссылкой")
        if not isinstance(self._salary_from, int) or self._salary_from < 0:
            raise ValueError("Зарплата должна быть положительным числом")
        if not isinstance(self._salary_to, int) or self._salary_to < 0:
            raise ValueError("Зарплата должна быть положительным числом")

    @property
    def avg_salary(self) -> int:
        """Вычисляет среднюю зарплату"""
        return (self._salary_from + self._salary_to) // 2 if self._salary_to else self._salary_from

    def __lt__(self, other) -> bool:
        """Сравнение вакансий по средней зарплате (меньше)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary < other.avg_salary

    def __gt__(self, other) -> bool:
        """Сравнение вакансий по средней зарплате (больше)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary > other.avg_salary

    def __eq__(self, other) -> bool:
        """Сравнение вакансий по средней зарплате (равно)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __repr__(self) -> str:
        return f"Vacancy(title='{self._title}', url='{self._url}')"

    @classmethod
    def cast_to_object_list(cls, data: List[Dict]) -> List["Vacancy"]:
        """Преобразует JSON-данные в список объектов Vacancy"""
        vacancies = []
        for item in data:
            salary = item.get("salary", {})
            vacancies.append(cls(
                title=item.get("name", ""),
                url=item.get("alternate_url", ""),
                salary_from=salary.get("from", 0),
                salary_to=salary.get("to", 0),
                description=item.get("description", ""),
                requirements=item.get("snippet", {}).get("requirement", "")
            ))
        return vacancies