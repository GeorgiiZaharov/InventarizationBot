import asyncio
from ollama import AsyncClient

class DataExtractor:
    def __init__(self, model: str = 'llama2'):
        self.model = model
        self.client = AsyncClient()

    # Функция для отправки сообщения модели и получения ответа
    async def get_model_response(self, prompt: str) -> str:
        # Создаем сообщение с ролями
        message = {
            'role': 'user',
            'content': prompt,
            'system_prompt': """
Ты анализируешь текст на Русском языке и выделяешь информацию, наиболее подходящую под переданный тебе запрос. Твой единственный фокус — извлечение данных из текста, без домыслов, догадок или интерпретации. Если информация не найдена, возвращай 'Null'.

Контекст: 
1. Ты работаешь с текстом, который может содержать различные типы данных: имена, номера кабинетов, адреса, описания, даты и т. д. 
2. У тебя нет задачи создавать новые данные или делать выводы. Всё, что ты возвращаешь, должно быть взято только из текста.

Формат ответа: 
1. Твой ответ должен быть кратким. Выводи только найденную часть текста, которая максимально соответствует запросу.
2. Если подходящая информация отсутствует, возвращай 'Null'.
3. Не добавляй комментариев, пояснений или текста вне контекста извлечения.
4. Твой вывод должен быть кратким и четким, так как результат твоей работы будет подаваться на вход другой программе.

Примеры: 
1. Текст: "к.301 Кравченко А.В. расписка, Невского, ИЛ"  
Запрос: "ответственное лицо"  
Ответ: "Кравченко А.В."
2. Текст: "к.128 Интернет"  
Запрос: "кабинет"  
Ответ: "к.128"
3. Текст: "к.209 ИПМИ Кузьменко (399?)"  
Запрос: "организация"  
Ответ: "ИПМИ"
4. Текст: "к.123 Психдиспансер"  
Запрос: "ответственное лицо"  
Ответ: "Null"
    """,
            'temperature': 0
        }
        
        # Отправляем запрос к серверу Ollama и получаем ответ
        response = await self.client.chat(model=self.model, messages=[message])
        
        # Возвращаем контент из ответа модели
        return response.message.content

    # Метод для извлечения ответственного лица
    async def get_responsible_person(self, data: str) -> str:
#         prompt = f"""
# Из текста необходимо выделить ответственное лицо, то есть человека, которому передан объект. Ответственное лицо может быть указано в виде полного имени, имени и фамилии, только имени, только фамилии, или может не быть упомянуто вовсе.
# Если ответственное лицо указано, вернуть его в том виде, как оно указано в тексте.
# Если ответственное лицо отсутствует, вернуть строку Null.
# Вот строка с данными для извлечения: {data}
# Ответ должен содержать только имя/фамилию/отчество/инициалы человека кому передан объект.
# Твой ответ будет использоваться другой программой, поэтому он должен быть кратким.
#         """
        prompt = f"Выдели ответсвенное лицо из этого текста, если такого нет напиши NULL. {data} Если возможны несколько вариантов, выбери один наиболее подходящий. НЕ ПИШИ НИЧЕГО КРОМЕ ОТВЕТА, так как твой вывод будет использоваться другой программой."
        response = await self.get_model_response(prompt)
        return response

    # Метод для извлечения места хранения
    async def get_storage_place(self, data: str) -> str:
        prompt = f"""
        Текст: "{data}"
        Запрос: "кабинет"
        """
        response = await self.get_model_response(prompt)
        return response


# Основная асинхронная функция
async def main():
    data = "к.209 ИПМИ Кузьменко (399?)"
    
    extractor = DataExtractor()  # Создаем экземпляр класса
    
    # Получаем ответственное лицо
    # responsible_person = await extractor.get_responsible_person(data)
    # print("Ответственное лицо:", responsible_person)  # Печатаем ответ от модели

    # Получаем место хранения
    storage_place = await extractor.get_storage_place(data)
    print("Место хранения:", storage_place)  # Печатаем ответ от модели


# Запуск основной функции
if __name__ == "__main__":
    asyncio.run(main())