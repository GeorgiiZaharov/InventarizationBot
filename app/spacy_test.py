import spacy
from typing import List, Dict

class NamedEntityRecognizer:
    """
    Класс для обработки текстов с помощью NER и выделения именованных сущностей.
    """
    
    def __init__(self, model_name: str = "ru_core_news_lg"):
        """
        Инициализация NER с загрузкой модели spaCy.
        """
        self.nlp = spacy.load(model_name)
    
    def extract_entities(self, text: str, entity_types: List[str] = None) -> List[Dict[str, str]]:
        """
        Извлекает сущности из текста с указанными типами.
        
        :param text: Исходный текст.
        :param entity_types: Список типов сущностей для извлечения (например, ["PERSON", "LOC"]).
                             Если None, извлекаются все сущности.
        :return: Список словарей, содержащих сущности с их типами.
        """
        if entity_types is None:
            entity_types = ["PER", "LOC"]
        
        doc = self.nlp(text)
        entities = [
            {"text": ent.text, "type": ent.label_}
            for ent in doc.ents
            if ent.label_ in entity_types
        ]
        
        # Пользовательская логика для обработки местоположений (например, "к. 104")
        entities.extend(self._extract_custom_locations(doc))
        return entities

    def _extract_custom_locations(self, doc: spacy.tokens.Doc) -> List[Dict[str, str]]:
        """
        Дополнительная обработка для извлечения местоположений, таких как "к. 104".
        """
        custom_locations = []
        for token in doc:
            if token.text.lower().startswith("к.") and token.i + 1 < len(doc):
                next_token = doc[token.i + 1]
                if next_token.like_num:
                    custom_locations.append(
                        {"text": f"{token.text} {next_token.text}", "type": "CUSTOM_LOC"}
                    )
        return custom_locations
if __name__ == "__main__":
    ner = NamedEntityRecognizer()
    text = "Андрей Петров работает в кабинете к. 104. Иванова A.A. находится в к. 202."
    
    extracted_entities = ner.extract_entities(text)
    print("Извлеченные сущности:")
    for entity in extracted_entities:
        print(f"Текст: {entity['text']}, Тип: {entity['type']}")
    nlp = spacy.load("ru_core_news_lg")

    doc = nlp("Мария Иванова пошла в парк в Доме.")
    for ent in doc.ents:
        print(ent.text, ent.label_)

