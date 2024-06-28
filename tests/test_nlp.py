# Pruebas unitarias para el procesamiento de lenguaje natural
import unittest
from nlp_processing.preprocessing import tokenize_text

class TestNLPProcessing(unittest.TestCase):
    def test_tokenize_text(self):
        text = "Educational content example."
        tokens = tokenize_text(text)
        self.assertIsInstance(tokens, list)
        self.assertEqual(tokens, ['Educational', 'content', 'example', '.'])

if __name__ == '__main__':
    unittest.main()
