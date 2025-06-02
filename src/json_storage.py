import json
from pathlib import Path
from typing import List, Dict
from src.vacancy import Vacancy
from src.abstract_storage import Storage


class JSONStorage(Storage):
    def __init__(self, file_path: str = "data/vacancies.json"):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self.file_path.parent.mkdir(exist_ok=True)
            self.file_path.write_text("[]", encoding="utf-8")

    def __read_vacancies(self) -> List[Dict]:
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def __write_vacancies(self, data: List[Dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.__read_vacancies()
        vacancies.append(vacancy.__dict__)
        self.__write_vacancies(vacancies)

    def get_vacancies(self, **filters) -> List[Vacancy]:
        vacancies_data = self.__read_vacancies()
        vacancies = [Vacancy(**data) for data in vacancies_data]

        if not filters:
            return vacancies

        filtered = []
        for vacancy in vacancies:
            if "keyword" in filters and filters["keyword"].lower() not in vacancy.description.lower():
                continue
            if "min_salary" in filters and vacancy.avg_salary < filters["min_salary"]:
                continue
            filtered.append(vacancy)
        return filtered

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.__read_vacancies()
        updated = [v for v in vacancies if v["url"] != vacancy.url]
        self.__write_vacancies(updated)
