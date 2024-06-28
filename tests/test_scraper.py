# Pruebas unitarias para la extracción de datos
import unittest
from data_extraction.scraper import extract_educational_content

class TestScraper(unittest.TestCase):
    def test_extract_educational_content(self):
        url = 'https://www.ejemplo.com'
        content = extract_educational_content(url)
        self.assertIsInstance(content, list)
        self.assertGreater(len(content), 0)

if __name__ == '__main__':
    unittest.main()
