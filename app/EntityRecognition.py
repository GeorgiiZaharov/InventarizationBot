from typing import List
import pandas as pd
import re

from DTOmodels import ItemDTO, MovementDTO

class OldFileParser:
    """
    Этот класс отвечает за парсинг старых инвентаризационных файлов и извлечение данных.
    """

    def __init__(self, path: str) -> None:
        """
        Инициализация парсера старых файлов инвентаризации с путем к файлу.

        Параметры:
        path (str): Путь к файлу инвентаризации.
        """
        self.path = path
    
    def get_items(self) -> List[ItemDTO]:
        """
        Парсинг файла инвентаризации и извлечение данных о предметах.

        Возвращает:
        List[ItemDTO]: Список объектов ItemDTO, представляющих извлеченные данные о предметах.
        """
        try:
            df = pd.read_excel(self.path)  # Чтение Excel файла
            res = []
            for _, note in df.iterrows():  # Проход по строкам DataFrame
                # Разделение информации о человеке и месте хранения
                responsible_person, storage_place = str(note['МОЛ/Место хранения']).split(' - ')
                item = ItemDTO(
                    name=str(note['Наименование']),
                    code=str(note['Код']),
                    card_number=str(note['Номер инвентарной карточки']),
                    inventory_number=str(note['Инвентарный номер']),
                    responsible_person=responsible_person,
                    storage_place=storage_place,
                    card_date=str(note['Дата инвентарной карточки']),
                    group_accounting=str(note['Групповой учет']),
                    condition=str(note['Состояние']),
                    accounting_account=str(note['Счет учета']),
                    KFO=str(note['КФО']),
                    KPS=str(note['КПС']),
                    property_type=str(note['Вид имущества']),
                    department=str(note['Подразделение'])
                )
                res.append(item)  # Добавление предмета в результат
            return res  
        except:
            return []  # Возвращаем пустой список в случае ошибки

    def get_movements(self) -> List[MovementDTO]:
        """
        Парсинг файла инвентаризации и извлечение данных о перемещениях.

        Возвращает:
        List[MovementDTO]: Список объектов MovementDTO, представляющих извлеченные данные о перемещениях.
        """
        try:
            df = pd.read_excel(self.path)  # Чтение Excel файла
            res = []
            for ind, note in df.iterrows():  # Проход по строкам DataFrame
                if not pd.isna(note['Местонахождение']):  # Проверка наличия местонахождения
                    location_dict = self.__parse_location(str(note['Местонахождение']))  # Парсинг местонахождения
                    movement = MovementDTO(
                        identifier=str(note['Код']),
                        new_location=location_dict['where'],
                        responsible_person=location_dict['whose'],
                        description=location_dict['description'],
                        transfer_time="00.00.0000"  # Время перемещения (по умолчанию)
                    )
                    res.append(movement)  # Добавление перемещения в результат
            return res
        except:
            return []  # Возвращаем пустой список в случае ошибки

    def __parse_name(self, entry: str) -> str:
        """
        Парсинг имени из заданной строки.

        Параметры:
        entry (str): Строка, содержащая имя.

        Возвращает:
        str: Извлеченное имя.
        """
        name_pattern = r'\b[A-ZА-Я][a-zа-я]+\s*(?:[A-ZА-Я](?:\.|[a-zа-я]+)?)?\s*(?:[A-ZА-Я](?:\.|[a-zа-я]+)?)?'
        person_pattern = re.compile(name_pattern, re.UNICODE)
        person_match = re.search(name_pattern, entry)

        person = person_match.group(0) if person_match else ''
        return person

    def __parse_cabinet_number(self, entry: str) -> dict:
        """
        Парсинг номера кабинета из заданной строки.

        Параметры:
        entry (str): Строка, содержащая номер кабинета.

        Возвращает:
        dict: Словарь с оригинальным и разобранным номером кабинета.
        """
        cabinet_pattern = re.compile(r'\b((?:(?:к\.|каб\.)\s*)?(\d{3}[-]?[А-ЯA-Zа-яa-z]?))', re.IGNORECASE)
        find_cabinet_number = re.findall(cabinet_pattern, entry)
        if find_cabinet_number:
            cabinet_number = find_cabinet_number[0][1]  # Внутреннее значение
            original = find_cabinet_number[0][0]  # Внешнее значение
            number = re.findall(r"(\d+)", cabinet_number)[0]
            if cabinet_number[-1].isalpha():
                cabinet_number = f"к.{number}{cabinet_number[-1].capitalize()}"
            else:
                cabinet_number = f"к.{number}"
        else:
            cabinet_number = ''
            original = ''
        return {
            "original": original,
            "result": cabinet_number
        }

    def __parse_location(self, entry: str) -> dict:
        """
        Парсинг местонахождения из заданной строки.

        Параметры:
        entry (str): Строка, содержащая местонахождение.

        Возвращает:
        dict: Словарь с разобранной информацией о местонахождении.
        """
        cabinet_number = self.__parse_cabinet_number(entry)  # Парсинг номера кабинета
        person_name = self.__parse_name(entry)  # Парсинг имени
        additional_info = entry  # Дополнительная информация о местонахождении

        if cabinet_number["result"]:
            additional_info = additional_info.replace(cabinet_number['original'], '')
            cabinet_number = cabinet_number['result']
        else:
            cabinet_number = additional_info
            additional_info = ''
        
        if person_name:
            additional_info = additional_info.replace(person_name, '')

        return {
            'where': cabinet_number,
            'whose': person_name,
            'description': additional_info.strip()
        }
