import unittest
import sys
import os

# Добавляем корень проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'NamedEntityRecognitionModels')))

# Импортируем тесты
from NamedEntityRecognitionModels.tests.RegexNamedEntityRecognizerTests import TestRegexNamedEntityRecognizer

if __name__ == '__main__':
    # Запускаем тесты
    unittest.main()
