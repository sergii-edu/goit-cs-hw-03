import curses
from tabulate import tabulate
from seed import create_tables, remove_tables, populate_database
from queries import (
    get_tasks_by_user,
    get_tasks_by_status,
    update_task_status,
    get_users_with_no_tasks,
    add_task_for_user,
    get_uncompleted_tasks,
    delete_task,
    find_users_by_email,
    update_user_name,
    get_task_count_by_status,
    get_tasks_for_email_domain,
    get_tasks_without_description,
    get_in_progress_tasks_and_users,
    get_users_and_their_task_counts,
)


def display_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(
        """
1. Створити таблиці та заповнити їх даними (включаючи видалення попередніх даних).

2. Отримати всі завдання певного користувача.
3. Вибрати завдання за певним статусом.
4. Оновити статус конкретного завдання.
5. Отримати список користувачів, які не мають жодного завдання.
6. Додати нове завдання для конкретного користувача.
7. Отримати всі завдання, які ще не завершено.
8. Видалити конкретне завдання.
9. Знайти користувачів з певною електронною поштою.
10. Оновити ім'я користувача.
11. Отримати кількість завдань для кожного статусу.
12. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
13. Отримати список завдань, що не мають опису.
14. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'.
15. Отримати користувачів та кількість їхніх завдань.

0. Вийти

Введіть опцію: """
    )


def display_data_in_table(stdscr, data, headers):
    if data:
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        stdscr.addstr(table + "\n")
    else:
        stdscr.addstr("Дані відсутні.\n")


def run_ui():
    def main(stdscr):
        curses.echo()
        stdscr.scrollok(True)
        stdscr.idlok(True)

        while True:
            display_menu(stdscr)
            option = stdscr.getstr().decode().strip()
            stdscr.clear()

            try:
                if option == "1":
                    remove_tables()
                    create_tables()
                    populate_database()
                    stdscr.addstr("\nТаблиці створені та заповнені.\n")

                elif option == "2":
                    tasks = get_tasks_by_user(
                        user_id=1,
                    )
                    display_data_in_table(
                        stdscr,
                        tasks,
                        ["ID", "Назва", "Опис", "ID статусу", "ID користувача"],
                    )

                elif option == "3":
                    tasks = get_tasks_by_status(status_name="new")
                    display_data_in_table(
                        stdscr,
                        tasks,
                        ["ID", "Назва", "Опис", "ID статусу", "ID користувача"],
                    )

                elif option == "4":
                    update_task_status(task_id=1, new_status="completed")
                    stdscr.addstr("\nСтатус завдання оновлено.\n")

                elif option == "5":
                    users = get_users_with_no_tasks()
                    display_data_in_table(
                        stdscr, users, ["ID", "Повне ім'я", "Електронна пошта"]
                    )

                elif option == "6":
                    add_task_for_user(
                        user_id=1,
                        title="Нове завдання",
                        description="Зробить щось",
                        status_id=1,
                    )
                    stdscr.addstr("\nНове завдання додано.\n")

                elif option == "7":
                    tasks = get_uncompleted_tasks()
                    display_data_in_table(
                        stdscr,
                        tasks,
                        ["ID", "Назва", "Опис", "ID статусу", "ID користувача"],
                    )

                elif option == "8":
                    delete_task(task_id=1)
                    stdscr.addstr("\nЗавдання видалено.\n")

                elif option == "9":
                    users = find_users_by_email(email_pattern="%@example.net%")
                    display_data_in_table(
                        stdscr, users, ["ID", "Повне ім'я", "Електронна пошта"]
                    )

                elif option == "10":
                    update_user_name(user_id=1, new_name="Іван Іваненко")
                    stdscr.addstr("\nІм'я користувача оновлено.\n")

                elif option == "11":
                    counts = get_task_count_by_status()
                    display_data_in_table(stdscr, counts, ["Статус", "Кількість"])

                elif option == "12":
                    tasks = get_tasks_for_email_domain(domain="example.com")
                    display_data_in_table(
                        stdscr,
                        tasks,
                        ["ID", "Назва", "Опис", "ID статусу", "ID користувача"],
                    )

                elif option == "13":
                    tasks = get_tasks_without_description()
                    display_data_in_table(stdscr, tasks, ["ID", "Назва"])

                elif option == "14":
                    users_tasks = get_in_progress_tasks_and_users()
                    display_data_in_table(
                        stdscr,
                        users_tasks,
                        [
                            "Повне ім'я",
                            "Назва",
                            "Опис",
                        ],
                    )

                elif option == "15":
                    users_tasks_counts = get_users_and_their_task_counts()
                    display_data_in_table(
                        stdscr, users_tasks_counts, ["Повне ім'я", "Кількість завдань"]
                    )

                elif option == "0":
                    break
                else:
                    stdscr.addstr("\nНевідома опція. Спробуйте знову.\n")
            except Exception as e:
                stdscr.addstr("\nПомилка: {}\n".format(e))

            stdscr.addstr("Натисніть будь-яку клавішу для продовження...")
            stdscr.getch()

    curses.wrapper(main)


if __name__ == "__main__":
    run_ui()
