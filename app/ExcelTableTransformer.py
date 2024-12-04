import asyncio
import pandas as pd
from openpyxl import Workbook
from NamedEntityRecognitionModels.RegexNamedEntityRecognizer import RegexNamedEntityRecognizer as NER

# Определение структуры старой таблицы
OLD_TABLE_STRUCTURE = [
    "Наименование",
    "Инвентарный номер",
    "МОЛ/Место хранения",
    "Местонахождение",
    "Дата инвентарной карточки",
    "Групповой учет",
    "Код",
    "Состояние",
    "Счет учета",
    "КФО",
    "КПС",
    "Вид имущества",
	"Подразделение",
    "Номер инвентарной карточки",
    "Ссылка"
]

# Определение структуры старой таблицы
NEW_TABLE_STRUCTURE = [
    "Наименование",
    "Инвентарный номер",
    "МОЛ",
    "Место хранения",
    "Местонахождение",
    "Ответственное лицо",
    "Дата инвентарной карточки",
    "Групповой учет",
    "Код",
    "Состояние",
    "Счет учета",
    "КФО",
    "КПС",
    "Вид имущества",
	"Подразделение",
    "Номер инвентарной карточки",
    "Заметка"
]

class ExcelTableTransformer:
    """
    Переводит данные из старой Excel таблицы в новый формат, который является промежутком между Excel и реляционной БД
    """
    def __init__(self, path: str) -> None:
        """
        Инициализация парсера старых файлов инвентаризации с путем к файлу.

        Args:
            path (str): Путь к файлу инвентаризации старого образца,
                наименование столбцов должно совпадать с OLD_TABLE_STRUCTURE.
        """
        self.path = path
        self.NER = NER
    
    async def transform(self, new_path: str) -> None:
        """
        Создает и заполняет новый файл, данные берутся из файла
        старого образца.
        Args:
            new_path (str): Путь к файлу с результатом трансформации,
                наименование столбцов будет 
        """
        wb = Workbook()
        sheet = wb.active
        sheet.append(NEW_TABLE_STRUCTURE)
        df = pd.read_excel(self.path)
        for _, note in df.iterrows():
            new_note_dict = await self.__transform_in_new_format(note)
            new_note = [new_note_dict[col] for col in NEW_TABLE_STRUCTURE]
            sheet.append(new_note)
        wb.save(new_path)

    
    async def __transform_in_new_format(self, note: dict) -> dict:
        """
        Из строки таблицы старого формата, возращает строку нового формата,
        ключи исходного словаря удовлетворяют формату NEW_TABLE_STRUCTURE
        Args:
            note (dict): словарь ключи которого удовлетворяют OLD_TABLE_STRUCTURE.
        Return:
            Возращает строку нового формата, ключи исходного словаря удовлетворяют формату NEW_TABLE_STRUCTURE
        """
        result = dict()
        MOL, storage_place = str(note["МОЛ/Место хранения"]).split(" - ")
        data = str(note["Местонахождение"])
        location = await self.NER.get_location(data + ' ' + note["Наименование"])
        responsibility_person = await self.NER.get_responsible_person(data)
        result["Наименование"] = str(note["Наименование"])
        result["Инвентарный номер"] = str(note["Инвентарный номер"])
        result["МОЛ"] = MOL
        result["Место хранения"] = storage_place
        result["Местонахождение"] = location
        result["Ответственное лицо"] = responsibility_person
        result["Дата инвентарной карточки"] = str(note["Дата инвентарной карточки"])
        result["Групповой учет"] = str(note["Групповой учет"])
        result["Код"] = str(note["Код"])
        result["Состояние"] = str(note["Состояние"])
        result["Счет учета"] = str(note["Счет учета"])
        result["КФО"] = str(note["КФО"])
        result["КПС"] = str(note["КПС"])
        result["Вид имущества"] = str(note["Вид имущества"])
        result["Подразделение"] = str(note["Подразделение"])
        result["Номер инвентарной карточки"] = str(note["Номер инвентарной карточки"])
        result["Заметка"] = data
        return result    


def main():
    excel_table_transfer = ExcelTableTransformer("/home/georgii/Projects/InventarizationBot/src/sample.xlsx")
    asyncio.run(excel_table_transfer.transform("/home/georgii/Projects/InventarizationBot/src/new.xlsx"))

if __name__ == "__main__":
    main()