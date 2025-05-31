 from src.vacancy import Vacancy


def test_vacancy_creation():
    v = Vacancy("Python Dev", "http://example.com", 100000, 150000, "Описание")
    assert v.title == "Python Dev"
    assert v.avg_salary == 125000


def test_vacancy_comparison():
    v1 = Vacancy("A", "http://1", 50000)
    v2 = Vacancy("B", "http://2", 100000)
    assert v2 > v1
