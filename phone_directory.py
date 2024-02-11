import os.path


def name_input(name: str) -> str:
    """Проверка и редактирование вводимых данных."""
    while True:
        input_name = input(f"Введите {name}: ")
        if input_name.isalpha() and not any(
            char.isdigit() or char.isspace() or char in "+-*/" for char in input_name
        ):
            return input_name.capitalize()
        else:
            print(f"Некорректный ввод. Параметр должен состоять из букв.")


def check_phone_input(phone: str) -> bool:
    """Проверка ввода телефонного номера."""
    return phone.isdigit()


def add_person(filename: str) -> str:
    """Добавление записи в справочник."""
    last_name = name_input("фамилию")
    name = name_input("имя")
    patronymic = name_input("отчество")
    organization = input("Введите организацию: ")
    personal_phone = input("Введите личный телефон: ")

    while not check_phone_input(personal_phone):
        print("Некорректный ввод. Пожалуйста, введите только цифры.")
        personal_phone = input("Введите личный телефон: ")

    work_phone = input("Введите рабочий телефон: ")

    while not check_phone_input(work_phone):
        print("Некорректный ввод. Пожалуйста, введите только цифры.")
        work_phone = input("Введите рабочий телефон: ")

    contact = f"{last_name};{name};{patronymic};{organization};{personal_phone};{work_phone}\n"
    with open(filename, "a+", encoding="utf8") as myfile:
        myfile.write(contact)
    return f"Контакт {contact} добавлен в телефонный справочник"


def search_edit_contact(filename: str, edit: bool) -> str:
    """Поиск контакта в справочнике."""
    search_name = name_input("фамилию")

    with open(filename, "r+", encoding="utf8") as myfile:
        contacts = myfile.readlines()

    for i, line in enumerate(contacts):
        if search_name in line:
            if edit:
                print(contacts[i])
                edit_contact = add_person(filename)
                contacts[i] = edit_contact
                return f"Контакт {search_name} изменён: {contacts[i]}"
            return f"Контакт {search_name} найден: {contacts[i]}"
    return f"Контатные данные {search_name} не найдены в справочнике."


def main_menu(filename: str) -> None:
    """Главное меню."""

    print("Главное меню")
    print("1. Показать все существующие контакты")
    print("2. Добавить новый контакт")
    print("3. Найти контакт")
    print("4. Редактировать контакт")
    print("5. Выход")

    choice = input("Введите число: ")
    if choice == "1":
        with open(filename, "r+", encoding="utf8") as myfile:
            contacts = myfile.read()
            if len(contacts) == 0:
                print("В справочнике пока нет контактов")
            else:
                print(contacts)
        enter = input("Нажмите Enter чтобы продолжить")
        main_menu(filename)
    elif choice == "2":
        contact = add_person(filename)
        print(f"{contact}\n")
        enter = input("Нажмите Enter чтобы продолжить")
        main_menu(filename)
    elif choice == "3":
        contact = search_edit_contact(filename, edit=False)
        print(f"{contact}\n")
        enter = input("Нажмите Enter чтобы продолжить")
        main_menu(filename)
    elif choice == "4":
        contact = search_edit_contact(filename, edit=True)
        print(f"{contact}\n")
        enter = input("Нажмите Enter чтобы продолжить")
        main_menu(filename)
    elif choice == "5":
        print("Спасибо что воспользовались телефонным справочником")
    else:
        print("Подтвердите ваш выбор")
        enter = input("Нажмите Enter чтобы продолжить")
        main_menu(filename)


if __name__ == "__main__":
    print("ДОБРО ПОЖАЛОВАТЬ В ТЕЛЕФОННЫЙ СПРАВОЧНИК")
    filename = "phone_directory.txt"
    if not os.path.exists(filename):
        table_name = "Фамилия;Имя;Отчество;Организация;Личный телефон;Рабочий телефон\n"
        with open(filename, "a+", encoding="utf8") as myfile:
            myfile.write(table_name)

    main_menu(filename)
