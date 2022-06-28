from functools import wraps
import datetime
from os import path, mkdir


def logger(old_function):
    """ Декоратор - логгер, записывает в файл "logs 1.log" дату и время вызова функции, имя функции,
        аргументы, с которыми вызвалась и возвращаемое значение.
        Путь к файлу: текущая директория -> logs -> logger -> logs 1.log

    :return: Возвращаемое значение задекорированной функии.
    """
    @wraps(old_function)
    def new_function(*args, **kwargs):
        start = datetime.datetime.now()
        result = old_function(*args, **kwargs)
        log = f"{start} function {old_function.__name__} is called with arguments" \
              f" *args = {args} and **kwargs = {kwargs}\n" \
              f"execution result: {result}\n\n"
        log_path = path.join("logs", "logger", "logs 1.log")
        if not path.exists("logs"):
            mkdir("logs")
        if not path.exists(path.join("logs", "logger")):
            mkdir(path.join("logs", "logger"))
        with open(log_path, "a", encoding="utf-8") as file:
            file.write(log)
        return result
    return new_function


def logger_with_param(path_to_logs="logs\logger with param"):
    """ Декоратор - логгер, записывает в файл "logs 2.log" дату и время вызова функции, имя функции,
        аргументы, с которыми вызвалась и возвращаемое значение.

    :param path_to_logs: Директория, в которую запишется файл с логами.
                         По умолчанию: текущая директория -> logs -> logger with param
    :return: Возвращаемое значение задекорированной функии.
    """
    def logger_2(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            lst = [path_to_logs]
            start = datetime.datetime.now()
            result = old_function(*args, **kwargs)
            log = f"{start} function {old_function.__name__} is called with arguments" \
                  f" *args = {args} and **kwargs = {kwargs}\n" \
                  f"execution result: {result}\n\n"

            while path.split(lst[0])[1]:
                lst.append(path.split(lst[0])[1])
                lst[0] = path.split(lst[0])[0]
            lst.append(lst.pop(0))
            if lst[-1] == "" or lst[-1] == "/" or lst[-1] == "\\":
                lst.pop()
            lst.reverse()
            path_logs = ""
            for item in lst:
                path_logs = path.join(path_logs, item)
                if not path.exists(path_logs):
                    mkdir(path_logs)
            path_logs = path.join(path_logs, "logs 2.log")
            with open(path_logs, "a", encoding="utf-8") as file:
                file.write(log)
            return result
        return new_function
    return logger_2
