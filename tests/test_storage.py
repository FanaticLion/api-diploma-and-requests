import json
import os
import pytest
from src.vacancy import Vacancy
from src.json_storage import JSONStorage


@pytest.fixture
def temp_json_file(tmp_path):
    """Фикстура для временного JSON-файла"""
    file_path = tmp_path / "test_vacancies.json"
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def storage(temp_json_file):
    """Фикстура для тестируемого хранилища"""
    return JSONStorage(file_path=str(temp_json_file))


@pytest.fixture
def sample_vacancies():
    """Фикстура для тестовых вакансий"""
    return [
        Vacancy("Python Dev", "http://example.com/1", 100000, 150000, "Python разработчик"),
        Vacancy("Java Dev", "http://example.com/2", 90000, 120000, "Java разработчик"),
        Vacancy("Data Scientist", "http://example.com/3", 150000, 200000, "Анализ данных"),
    ]


def test_add_vacancy(storage, sample_vacancies):
    """Проверка добавления вакансии в файл"""
    storage.add_vacancy(sample_vacancies[0])
    assert len(storage.get_vacancies()) == 1


def test_get_vacancies_empty(storage):
    """Проверка получения вакансий из пустого файла"""
    assert not storage.get_vacancies()


def test_get_vacancies_with_data(storage, sample_vacancies):
    """Проверка получения всех вакансий"""
    for vacancy in sample_vacancies:
        storage.add_vacancy(vacancy)
    assert len(storage.get_vacancies()) == 3


def test_filter_vacancies_by_keyword(storage, sample_vacancies):
    """Проверка фильтрации по ключевому слову"""
    for vacancy in sample_vacancies:
        storage.add_vacancy(vacancy)
    filtered = storage.get_vacancies(keyword="Python")
    assert len(filtered) == 1 and filtered[0].title == "Python Dev"


def test_filter_vacancies_by_salary(storage, sample_vacancies):
    """Проверка фильтрации по зарплате"""
    for vacancy in sample_vacancies:
        storage.add_vacancy(vacancy)
    filtered = storage.get_vacancies(min_salary=110000)
    assert len(filtered) == 2
    assert {v.title for v in filtered} == {"Python Dev", "Data Scientist"}


def test_delete_vacancy(storage, sample_vacancies):
    """Проверка удаления вакансии"""
    for vacancy in sample_vacancies:
        storage.add_vacancy(vacancy)
    storage.delete_vacancy(sample_vacancies[1])
    remaining = storage.get_vacancies()
    assert len(remaining) == 2 and all(v.url != "http://example.com/2" for v in remaining)


def test_file_creation_if_not_exists(temp_json_file):
    """Проверка создания файла, если его нет"""
    assert not os.path.exists(temp_json_file)
    storage_instance = JSONStorage(file_path=str(temp_json_file))
    assert os.path.exists(temp_json_file) and not storage_instance.get_vacancies()


def test_empty_file_initialization(temp_json_file):
    """Проверка инициализации пустого файла"""
    storage_instance = JSONStorage(file_path=str(temp_json_file))
    with open(temp_json_file, "r", encoding="utf-8") as f:
        assert json.load(f) == []
