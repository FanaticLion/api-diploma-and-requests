from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy
from src.json_storage import JSONStorage


def user_interaction():
    print("🔍 Поиск вакансий на hh.ru")
    query = input("Введите запрос (например, 'Python разработчик'): ")
    top_n = int(input("Сколько вакансий вывести в топ? "))
    keyword = input("Ключевое слово для фильтрации (Enter - пропустить): ")
    min_salary = int(input("Минимальная зарплата (0 - не учитывать): "))

    # Получаем вакансии
    hh_api = HeadHunterAPI()
    try:
        vacancies_data = hh_api.get_vacancies(query, 100)
        vacancies = Vacancy.cast_to_object_list(vacancies_data)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return

    # Сохраняем и фильтруем
    storage = JSONStorage()
    for vacancy in vacancies:
        storage.add_vacancy(vacancy)

    filtered = storage.get_vacancies(
        keyword=keyword if keyword else None,
        min_salary=min_salary if min_salary > 0 else None,
    )

    # Сортируем по зарплате и выводим топ-N
    top_vacancies = sorted(filtered, key=lambda v: v.avg_salary, reverse=True)[:top_n]

    print(f"\n🔎 Найдено {len(top_vacancies)} вакансий:")
    for i, vacancy in enumerate(top_vacancies, 1):
        print(f"{i}. {vacancy.title} | {vacancy.salary_from}-{vacancy.salary_to} ₽")
        print(f"   📌 {vacancy.description[:100]}...")
        print(f"   🔗 {vacancy.url}\n")


if __name__ == "__main__":
    user_interaction()
