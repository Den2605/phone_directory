import os.path
from typing import Dict, List, Tuple

from tabulate import tabulate


def load_contacts(filename: str) -> List[List[str]]:
    """Загрузка и сортировка контактов из файла."""
    with open(filename, "r", encoding="utf8") as myfile:
        contacts = myfile.readlines()
        if contacts:
            contacts = [contact.split(";") for contact in contacts]
            contacts = sorted(contacts)
            return contacts


def display_contacts(contacts: List[List[str]]) -> None:
    """Вывод контактов в консоль."""
    if contacts:
        headers: List[str] = [
            "Фамилия",
            "Имя",
            "Отчество",
            "Организация",
            "Личный телефон",
            "Рабочий телефон",
        ]
        print(tabulate(contacts, headers=headers))
    else:
        print("Данных нет.")


def name_input(name: str) -> str:
    """Проверка и редактирование вводимых данных."""
    while True:
        input_name: str = input(f"Введите {name}: ").strip()
        if input_name.isalpha() and not any(
            char.isdigit() or char.isspace() or char in "+-*/" for char in input_name
        ):
            return input_name.capitalize()
        else:
            print(f"Некорректный ввод. Параметр должен состоять из букв.")


def phone_input(type_phone: str) -> str:
    """Проверка ввода телефонного номера."""
    while True:
        phone: str = input(f"Введите {type_phone} : ").strip()
        if phone.isdigit():
            return phone
        else:
            print("Некорректный ввод. Пожалуйста, введите только цифры.")


def input_contact_data() -> str:
    """Ввод контактных данных."""
    last_name: str = name_input("фамилию")
    name: str = name_input("имя")
    patronymic: str = name_input("отчество")
    organization: str = input("Введите организацию: ")
    personal_phone: str = phone_input("личный")
    work_phone: str = phone_input("рабочий")
    return f"{last_name};{name};{patronymic};{organization};{personal_phone};{work_phone}\n"


def add_person(filename: str) -> List[List[str]]:
    """Добавление записи в справочник."""
    contact: str = input_contact_data()
    with open(filename, "a+", encoding="utf8") as myfile:
        myfile.write(contact)
    return [contact.split(";")]


def input_search_data() -> Dict[str, str]:
    """Ввод данных для поиска."""
    search_criteria: Dict[str, str] = {}
    search_criteria["last_name"] = input(
        "Введите фамилию или оставьте пустым: "
    ).strip()
    search_criteria["name"] = input("Введите имя или оставьте пустым: ").strip()
    search_criteria["patronymic"] = input(
        "Введите отчество или оставьте пустым: "
    ).strip()
    search_criteria["organization"] = input(
        "Введите организацию или оставьте пустым: "
    ).strip()
    search_criteria["personal_phone"] = input(
        "Введите личный телефон или оставьте пустым: "
    ).strip()
    search_criteria["work_phone"] = input(
        "Введите рабочий телефон или оставьте пустым: "
    ).strip()
    return search_criteria


def search_edit_contact(filename: str, edit: bool) -> List[List[str]]:
    """Поиск контакта в справочнике."""
    search_criteria: Dict[str, str] = input_search_data()
    with open(filename, "r+", encoding="utf8") as myfile:
        contacts: List[str] = myfile.readlines()
        if contacts:
            search_contacts_list: List[Tuple[str, int]] = []
            contacts = [contact.split(";") for contact in contacts]
            for line, contact in enumerate(contacts):
                match: bool = True
                for key, value in search_criteria.items():
                    if value:
                        index: int = {
                            "last_name": 0,
                            "name": 1,
                            "patronymic": 2,
                            "organization": 3,
                            "personal_phone": 4,
                            "work_phone": 5,
                        }[key]
                        if contact[index].strip() != value:
                            match = False
                            break
                if match:
                    search_contacts_list.append([contact, line])
            first_elements: List[str] = [contact[0] for contact in search_contacts_list]
            # поиск
            if edit == False:
                return sorted(first_elements)
            # редактирование
            else:
                if search_contacts_list:
                    count: int = len(search_contacts_list)
                    display_contacts(first_elements)
                    number: int = 0
                    # выбираем контакт для редактирования
                    while True:
                        number_str: str = input(
                            f"Введите номер элемента от 1 до {count}: "
                        )
                        if number_str.isdigit():
                            number = int(number_str)
                            if 1 <= number <= count:
                                break
                    change_line: int = search_contacts_list[number - 1][1]

                    # отображаем выбранный контакт
                    print(search_contacts_list[number - 1][0])
                    print(search_contacts_list[number - 1][1])
                    changed_contact: str = input_contact_data()
                    # создаем список и записываем в контакты
                    contacts[change_line] = changed_contact.split(";")
                    # перезаписываем файл
                    myfile.seek(0)
                    myfile.truncate()
                    myfile.writelines(";".join(contact) for contact in contacts)
                    return [contacts[change_line]]


def main_menu(filename: str) -> None:
    """Главное меню."""

    print("Главное меню")
    print("1. Показать все существующие контакты")
    print("2. Добавить новый контакт")
    print("3. Найти контакт")
    print("4. Редактировать контакт")
    print("5. Выход")

    choice: str = input("Введите число: ")
    if choice == "1":
        contacts: List[List[str]] = load_contacts(filename)
        display_contacts(contacts)
        enter: str = input("Нажмите Enter чтобы продолжить")
        main_menu(filename)
    elif choice == "2":
        contact: List[List[str]] = add_person(filename)
        print(f"Контакт добавлен в телефонный справочник")
        display_contacts(contact)
        enter = input("Нажмите Enter чтобы продолжить")
        main_menu(filename)
    elif choice == "3":
        contacts = search_edit_contact(filename, edit=False)
        display_contacts(contacts)
        enter = input("Нажмите Enter чтобы продолжить")
        main_menu(filename)
    elif choice == "4":
        contact = search_edit_contact(filename, edit=True)
        display_contacts(contact)
        enter = input("Нажмите Enter чтобы продолжить")
        main_menu(filename)
    elif choice == "5":
        print("Спасибо что воспользовались телефонным справочником")
    else:
        print("Неверный ввод.")
        enter = input("Нажмите Enter чтобы продолжить")
        main_menu(filename)


if __name__ == "__main__":
    print("ДОБРО ПОЖАЛОВАТЬ В ТЕЛЕФОННЫЙ СПРАВОЧНИК")
    filename: str = "phone_directory.csv"
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf8") as myfile:
            pass
    main_menu(filename)
