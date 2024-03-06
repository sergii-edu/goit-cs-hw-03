from db import get_db_connection
from tabulate import tabulate


def show_as_table(data):
    return tabulate(data, headers=["Ім'я", "Вік", "Характеристики"], tablefmt="pretty")


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Сталася помилка: {e}")
            raise

    return wrapper


@handle_exceptions
def add_cat_func(name, age, features):
    cats_collection = get_db_connection()
    features_list = [
        feature.strip() for feature in features.split(",") if feature.strip()
    ]
    cat_document = {"name": name, "age": age, "features": features_list}
    result = cats_collection.insert_one(cat_document)
    return f"Кіт доданий з ідентифікатором: {result.inserted_id}"


@handle_exceptions
def fetch_all_cats_func():
    cats_collection = get_db_connection()
    cats = cats_collection.find()
    data = [[doc["name"], doc["age"], ", ".join(doc["features"])] for doc in cats]
    return show_as_table(data)


@handle_exceptions
def fetch_cat_by_name_func(name):
    cats_collection = get_db_connection()
    cat = cats_collection.find_one({"name": name})
    if cat:
        data = [[cat["name"], cat["age"], ", ".join(cat["features"])]]
        return show_as_table(data)
    else:
        return "Кіт з таким ім'ям не знайдений."


@handle_exceptions
def update_cat_age_func(name, new_age):
    cats_collection = get_db_connection()
    result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.modified_count:
        return "Інформація про вік кота оновлена."
    else:
        return "Оновлення не відбулося. Перевірте ім'я кота."


@handle_exceptions
def add_feature_to_cat_func(name, feature):
    cats_collection = get_db_connection()
    result = cats_collection.update_one(
        {"name": name}, {"$addToSet": {"features": feature}}
    )
    if result.modified_count:
        return "Нова характеристика додана."
    else:
        return "Оновлення не відбулося. Можливо, кіт з таким ім'ям не існує або характеристика вже присутня."


@handle_exceptions
def delete_cat_by_name_func(name):
    cats_collection = get_db_connection()
    result = cats_collection.delete_one({"name": name})
    if result.deleted_count:
        return "Кіт успішно видалений."
    else:
        return "Кота з таким ім'ям не знайдено."


@handle_exceptions
def delete_all_cats_func():
    cats_collection = get_db_connection()
    result = cats_collection.delete_many({})
    return f"Видалено {result.deleted_count} котів."
