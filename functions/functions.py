import re
import csv
from functions.decorators import logger, logger_with_param


@logger_with_param(path_to_logs="logs\logger with param")
@logger
def reading_phonebook(path_phonebook: str) -> list:
    """ Считывает файл формата CSV и сохраняет данные в виде списка

    :param path_phonebook: Путь и/или имя файла, который необходимо прочитать
    :return: Данные из файла в виде списка
    """
    with open(path_phonebook, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list_def = list(rows)
    return contacts_list_def


@logger_with_param()
@logger
def write_phonebook(path_phonebook: str, contacts_list_def: list) -> None:
    """ Записывает данные из списка в файл формата CSV

    :param path_phonebook: Путь и/или имя файла, который будет записан
    :param contacts_list_def: Список, который будет записан в файл
    :return: None
    """
    with open(path_phonebook, "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list_def)


@logger_with_param()
@logger
def fixing_phonebook(contacts_list_def: list) -> None:
    """ Чинит адресную книгу

    Помещает ФИО в соответствующие поля. Приводит все телефоны в формат +7(999)999-99-99.
    Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999
    Объединяет все дублирующиеся записи о человеке в одну.

    :param contacts_list_def: Список, который нужно преобразовать
    :return: None
    """
    for person in contacts_list_def[1:]:
        # Приводим ФИО к требуемому формату
        full_name = (' '.join(person[0:3])).strip()
        pattern_1 = "[А-ЯЁ-]+"
        word_count = len(re.findall(pattern_1, full_name, re.I))
        person[0:word_count] = (re.findall(pattern_1, full_name, re.I))

        # Приводим телефон к требуемому формату
        pattern_2 = "(\+7|8)?[\s()-]*(\d{3})[\s()-]*(\d{3})[\s()-]*(\d{2})[\s()-]*(\d{2})[^,0-9]*(\d*)[^,0-9]*"
        prog = re.compile(pattern_2, re.I)
        rez = prog.search(person[5])
        if rez:
            if rez.group(6):
                person[5] = prog.sub(r"+7(\2)\3-\4-\5 доб.\6", person[5])
            else:
                person[5] = prog.sub(r"+7(\2)\3-\4-\5", person[5])

    # Объединяем все дублирующиеся записи о человеке в одну
    duplicates = []
    for counter, person in enumerate(contacts_list_def[1:-1], 2):
        for counter_next, person_next in enumerate(contacts_list_def[counter:]):
            if person[0:1] == person_next[0:1]:
                for column in range(2, 7):
                    if person[column] == "" and person_next[column] != "":
                        person[column] = person_next[column]
                duplicates.append(counter + counter_next)
    for counter, index_duplicates in enumerate(duplicates):
        contacts_list_def.pop(index_duplicates - counter)


@logger_with_param()
@logger
def print_phonebook(contacts_list_def: list) -> None:
    """ Построчный вывод на печать

    :param contacts_list_def: Список, который надо распечатать
    :return: None
    """
    for person in contacts_list_def:
        print(person)
