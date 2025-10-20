# your_app/tests/test_embeddings.py
from django.test import TestCase
from unittest.mock import patch
from helper.embedding import get_embedding  # مسیر رو با اسم اپ واقعی‌ات جایگزین کن

class EmbeddingTestCase(TestCase):

    def test_valid_text_returns_list_of_floats(self):
        text = ["this is a test"]
        embedding = get_embedding(text)
        self.assertIsInstance(embedding, list)
        self.assertGreater(len(embedding), 0)
        self.assertTrue(all(isinstance(x, float) for x in embedding))
        # برای bge-m3، طول معمولاً 1024 است
        self.assertEqual(len(embedding), 1024)

    def test_empty_string_raises_value_error(self):
        with self.assertRaises(ValueError) as cm:
            get_embedding("")
        self.assertIn("متن ورودی خالی است", str(cm.exception))

    def test_whitespace_only_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_embedding("   \t\n  ")

    def test_non_string_input_converted_to_string(self):
        # مثلاً عدد
        embedding = get_embedding(123)
        self.assertIsInstance(embedding, list)
        self.assertGreater(len(embedding), 0)

    @patch('helper.embedding.embedding_model.encode')
    def test_model_exception_raises_value_error(self, mock_encode):
        mock_encode.side_effect = Exception("Model failed")
        with self.assertRaises(ValueError) as cm:
            get_embedding("متن تست")
        self.assertIn("خطا در تولید Embedding", str(cm.exception))

    def test_embedding_is_normalized(self):
        import math
        text = "تست نرمال‌سازی"
        emb = get_embedding(text)
        norm = math.sqrt(sum(x * x for x in emb))
        self.assertAlmostEqual(norm, 1.0, places=6)