from dataclasses import dataclass, field
from typing import List, Dict


@dataclass(order=True)
class Vacancy:
    """Класс для представления вакансии"""
    title: str
    url: str
    salary_from: int = field(default=0, compare=False)
    salary_to: int = field(default=0, compare=False)
    description: str = field(default="", compare=False)

    @property
    def avg_salary(self) -> int:
        """Средняя зарплата (для сравнения)"""
        return (self.salary_from + self.salary_to) // 2 if self.salary_to else self.salary_from

    @classmethod
    def cast_to_object_list(cls, data: List[Dict]) -> List["Vacancy"]:
        """Преобразование JSON в список вакансий"""
        vacancies = []
        for item in data:
            salary = item.get("salary", {})
            vacancies.append(
                cls(
                    title=item.get("name", ""),
                    url=item.get("alternate_url", ""),
                    salary_from=salary.get("from", 0),
                    salary_to=salary.get("to", 0),
                    description=item.get("description", ""),
                )
            )
        return vacancies
