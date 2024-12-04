from NamedEntitiyRecognizer import NameEntityRecognition
import re

class RegexNamedEntityRecognizer(NameEntityRecognition):
    async def get_storage_place(self, data: str) -> str:
        """
        Метод для извлечения номера кабинета из строки.

        Он ищет шаблон, который соответствует номерам кабинетов.
        Форматы кабинетов могут включать 'к.' или 'каб.' перед числовым значением.
        Например, 'к.301' или 'каб.301' или 'к.301 А' могут быть распознаны.

        Аргументы:
            data (str): Строка с данными, из которой нужно извлечь номер кабинета.

        Возвращает:
            str: Номер кабинета или 'Null', если номер не найден.
        """

        cabinet_pattern = re.compile(r'\b((?:(?:к\.|каб\.)\s*)?(\d{3}[-]?[А-ЯA-Zа-яa-z]?))\b', re.IGNORECASE)
        find_cabinet_number = re.findall(cabinet_pattern, data)

        # Если найден номер кабинета, возвращаем его.
        # Если нет, возвращаем 'Null'.
        if find_cabinet_number:
            cabinet_number = find_cabinet_number[0][1]
            return cabinet_number
        return 'Null'

    async def get_responsible_person(self, data: str) -> str:
        """
        Метод для извлечения имени ответственного лица из строки.

        Он ищет шаблон, который соответствует именам и фамилиям.
        Строка должна содержать полное имя или фамилию с инициалами.

        Аргументы:
            data (str): Строка с данными, из которой нужно извлечь имя ответственного лица.

        Возвращает:
            str: Имя ответственного лица или 'Null', если имя не найдено.
        """

        name_pattern = r'\b[A-ZА-Я][a-zа-я]+\s*(?:[A-ZА-Я](?:\.|[a-zа-я]+)?)?\s*(?:[A-ZА-Я](?:\.|[a-zа-я]+)?)?'
        person_match = re.search(name_pattern, data)

        # Если найдено имя, возвращаем его. Если нет, возвращаем 'Null'.
        person = person_match.group(0) if person_match else 'Null'
        return person