# Pruebas unitarias para los sistemas de recomendación
import unittest
from recommendation.content_based_filtering import recommend_content

class TestRecommendation(unittest.TestCase):
    def test_recommend_content(self):
        documents = [
            "Educational content about Python.",
            "Advanced Python programming techniques.",
            "Basics of machine learning."
        ]
        query = "Python programming"
        recommendations = recommend_content(documents, query)
        self.assertIsInstance(recommendations, list)
        self.assertGreaterEqual(len(recommendations), 1)

if __name__ == '__main__':
    unittest.main()
