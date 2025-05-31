from src.hh_api import HeadHunterAPI


def test_hh_api_connection():
    api = HeadHunterAPI()
    api.connect()  # Если упадёт, тест провалится


def test_hh_api_get_vacancies():
    api = HeadHunterAPI()
    vacancies = api.get_vacancies("Python", 10)
    assert isinstance(vacancies, list)
