import unittest
import asyncio
from ..RegexNamedEntityRecognizer import RegexNamedEntityRecognizer

class TestRegexNamedEntityRecognizer(unittest.TestCase):
    def test_get_location(self):
        recognizer = RegexNamedEntityRecognizer()

        # Тестируем извлечение номера кабинета
        data1 = "к.301a Кравченко А.В. расписка"
        data2 = "каб.128 интернет"
        data3 = "к. 12 номер кабинета должен созержать 3 цифры"
        data4 = "Нет номера кабинета"
        data5 = "Каб. 128 интернет"
        data6 = "К123 без раздеителя"
        data7 = "8960123 просто цифры"
                
        # Проверяем правильный результат для разных вариантов
        result1 = asyncio.run(recognizer.get_location(data1))
        result2 = asyncio.run(recognizer.get_location(data2))
        result3 = asyncio.run(recognizer.get_location(data3))
        result4 = asyncio.run(recognizer.get_location(data4))
        result5 = asyncio.run(recognizer.get_location(data5))
        result6 = asyncio.run(recognizer.get_location(data6))
        result7 = asyncio.run(recognizer.get_location(data7))

        
        self.assertEqual(result1, "301a")  # Ожидаем номер кабинета "301a"
        self.assertEqual(result2, "128")  # Ожидаем номер кабинета "128"
        self.assertEqual(result3, "Null")    # Ожидаем "Null"
        self.assertEqual(result4, "Null")  # Ожидаем "Null"
        self.assertEqual(result5, "128")  # Ожидаем номер кабинета "128"
        self.assertEqual(result6, "Null")   # Ожидаем "Null"
        self.assertEqual(result7, "Null")   # Ожидаем "Null"



    
    def test_get_responsible_person(self):
        recognizer = RegexNamedEntityRecognizer()

        # Тестируем извлечение ответственного лица
        data1 = "к.301 Ленин А.В. расписка"
        data2 = "Иванов И.И."
        data3 = "не указано ответственное лицо"
        data4 = "Иванов И. И."
        data5 = "И.И.Иванов надо доработать!!" #TODO
        
        # Проверяем правильный результат для разных вариантов
        result1 = asyncio.run(recognizer.get_responsible_person(data1))
        result2 = asyncio.run(recognizer.get_responsible_person(data2))
        result3 = asyncio.run(recognizer.get_responsible_person(data3))
        result4 = asyncio.run(recognizer.get_responsible_person(data4))
        result5 = asyncio.run(recognizer.get_responsible_person(data5))

        
        self.assertEqual(result1, "Ленин А.В.")  # Ожидаем ответственного "Ленин А.В."
        self.assertEqual(result2, "Иванов И.И.")  # Ожидаем ответственного "Иванов И.И."
        self.assertEqual(result3, "Null")  # Ответственное лицо не указано, ожидаем "Null"
        self.assertEqual(result4, "Иванов И. И.")  # Ожидаем ответственного "Иванов И. И."
        self.assertEqual(result5, "Иванов")  # Ожидаем ответственного "Иванов"
