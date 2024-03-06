import curses

from functions import (
    add_cat_func,
    fetch_all_cats_func,
    fetch_cat_by_name_func,
    update_cat_age_func,
    add_feature_to_cat_func,
    delete_cat_by_name_func,
    delete_all_cats_func,
)


def add_cat(stdscr, add_cat_func):
    stdscr.addstr("Введіть ім'я кота: ")
    name = stdscr.getstr().decode()
    if not name:
        stdscr.addstr("\nІм'я не може бути пустим. Спробуйте ще раз.\n")
        return

    stdscr.addstr("Введіть вік кота: ")
    try:
        age = int(stdscr.getstr().decode())
    except ValueError:
        stdscr.addstr("\nВік повинен бути числом. Спробуйте ще раз.\n")
        return

    stdscr.addstr("Введіть характеристики кота (розділені комою): ")
    features = stdscr.getstr().decode()

    result = add_cat_func(name, age, features)
    stdscr.addstr(f"\n{result}\n")


def show_all_cats(stdscr, fetch_all_cats_func):
    cats_info = fetch_all_cats_func()
    stdscr.addstr(f"\n{cats_info}\n")


def find_cat(stdscr, fetch_cat_by_name_func):
    stdscr.addstr("Введіть ім'я кота для пошуку: ")
    name = stdscr.getstr().decode()
    if not name:
        stdscr.addstr("\nІм'я не може бути пустим. Спробуйте ще раз.\n")
        return

    result = fetch_cat_by_name_func(name)
    stdscr.addstr(f"\n{result}\n")


def update_cat_age(stdscr, update_cat_age_func):
    stdscr.addstr("Введіть ім'я кота для оновлення віку: ")
    name = stdscr.getstr().decode()
    if not name:
        stdscr.addstr("\nІм'я не може бути пустим. Спробуйте ще раз.\n")
        return

    stdscr.addstr("Введіть новий вік кота: ")
    try:
        new_age = int(stdscr.getstr().decode())
    except ValueError:
        stdscr.addstr("\nВік повинен бути числом. Спробуйте ще раз.\n")
        return

    result = update_cat_age_func(name, new_age)
    stdscr.addstr(f"\n{result}\n")


def add_feature_to_cat(stdscr, add_feature_to_cat_func):
    stdscr.addstr("Введіть ім'я кота для додавання характеристики: ")
    name = stdscr.getstr().decode()
    if not name:
        stdscr.addstr("\nІм'я не може бути пустим. Спробуйте ще раз.\n")
        return

    stdscr.addstr("Введіть характеристику для додавання: ")
    feature = stdscr.getstr().decode()

    result = add_feature_to_cat_func(name, feature)
    stdscr.addstr(f"\n{result}\n")


def delete_cat(stdscr, delete_cat_by_name_func):
    stdscr.addstr("Введіть ім'я кота для видалення: ")
    name = stdscr.getstr().decode()
    if not name:
        stdscr.addstr("\nІм'я не може бути пустим. Спробуйте ще раз.\n")
        return

    result = delete_cat_by_name_func(name)
    stdscr.addstr(f"\n{result}\n")


def delete_all_cats(stdscr, delete_all_cats_func):
    stdscr.addstr("Ви впевнені, що хочете видалити всіх котів? (так/ні): ")
    confirmation = stdscr.getstr().decode()
    if confirmation.lower() == "так":
        result = delete_all_cats_func()
        stdscr.addstr(f"\n{result}\n")
    else:
        stdscr.addstr("\nВидалення скасовано.\n")


def display_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(
        "1. Показати всіх котів"
        + "\n2. Додати кота"
        + "\n3. Знайти кота за ім'ям"
        + "\n4. Оновити вік кота"
        + "\n5. Додати характеристику коту"
        + "\n6. Видалити кота за ім'ям"
        + "\n7. Видалити всіх котів"
        + "\n0. Вийти"
        + "\nВиберіть опцію: "
    )


def run_ui():
    def main(stdscr):
        curses.echo()

        while True:
            display_menu(stdscr)
            option = stdscr.getstr().decode()
            stdscr.clear()
            stdscr.scrollok(True)

            if option == "1":
                show_all_cats(stdscr, fetch_all_cats_func)
            elif option == "2":
                add_cat(stdscr, add_cat_func)
            elif option == "3":
                find_cat(stdscr, fetch_cat_by_name_func)
            elif option == "4":
                update_cat_age(stdscr, update_cat_age_func)
            elif option == "5":
                add_feature_to_cat(stdscr, add_feature_to_cat_func)
            elif option == "6":
                delete_cat(stdscr, delete_cat_by_name_func)
            elif option == "7":
                delete_all_cats(stdscr, delete_all_cats_func)
            elif option == "0":
                break
            else:
                stdscr.addstr("\nНевідома опція. Спробуйте ще раз.\n")

            stdscr.addstr("Натисніть будь-яку клавішу для продовження...")
            stdscr.getch()

    curses.wrapper(main)


if __name__ == "__main__":
    run_ui()
