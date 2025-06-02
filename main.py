from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy
from src.json_storage import JSONStorage

def user_interaction():
    """Функция для взаимодействия с пользователем"""
    try:
        print("🔍 Поиск вакансий на hh.ru")
        query = input("Введите запрос (например, 'Python разработчик'): ")
        if not query:
            raise ValueError("Поисковый запрос не может быть пустым")

        try:
            top_n = int(input("Сколько вакансий вывести в топ? "))
        except ValueError:
            top_n = 10  # Значение по умолчанию

        keyword = input("Ключевое слово для фильтрации (Enter - пропустить): ")

        try:
            min_salary = int(input("Минимальная зарплата (0 - не учитывать): "))
        except ValueError:
            min_salary = 0  # Значение по умолчанию

        # Получение вакансий
        hh_api = HeadHunterAPI()
        vacancies_json = hh_api.get_vacancies(query, 100)
        vacancies = Vacancy.cast_to_object_list(vacancies_json)

        # Сохранение и фильтрация
        storage = JSONStorage()
        for vacancy in vacancies:
            storage.add_vacancy(vacancy)

        filtered = storage.get_vacancies(
            keyword=keyword if keyword else None,
            min_salary=min_salary if min_salary > 0 else None,
        )

        if not filtered:
            print("\n⚠️ По указанным критериям вакансии не найдены")
            return

        # Сортировка и вывод топ-N
        sorted_vacancies = sorted(filtered, reverse=True)[:top_n]
        print(f"\n🔎 Найдено {len(sorted_vacancies)} вакансий:")
        for i, vacancy in enumerate(sorted_vacancies, 1):
            print(f"{i}. {vacancy.title}")
            print(f"   💰 Зарплата: {vacancy.salary_from}-{vacancy.salary_to} ₽")
            print(f"   📌 Требования: {vacancy.requirements[:100]}...")
            print(f"   🔗 Ссылка: {vacancy.url}\n")

    except Exception as e:
        print(f"\n❌ Ошибка: {str(e)}")

if __name__ == "__main__":
    user_interaction()