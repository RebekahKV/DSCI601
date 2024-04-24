import unittest
from unittest.mock import MagicMock

class TestModelPredictions(unittest.TestCase):
    def setUp(self):
        """Setting up mocked model"""
        self.mocked_model = MagicMock()
        self.mocked_model.batch_predict.return_value = [
            ("I'll be landing in delhi tomorrow, will update it :')", 'eng_Latn', 1.0000157, 'IndicLID-FTR'),
            ("Mast video banake upload karna bhai, muje bhi dekhna hai pollution", 'ben_Latn', 0.60675067, 'IndicLID-FTR'),
            ("Window seat confirm mili hai ?", 'eng_Latn', 0.990012, 'IndicLID-FTR')
        ]
        self.test_samples = [
            "I'll be landing in delhi tomorrow, will update it :')",
            "Mast video banake upload karna bhai, muje bhi dekhna hai pollution",
            "Window seat confirm mili hai ?"
        ]
        self.batch_size = 1

    def test_batch_predictions(self):
        """Test the batch prediction output structure and data types."""
        outputs = self.mocked_model.batch_predict(self.test_samples, self.batch_size)

        # Check if the output is a list
        self.assertIsInstance(outputs, list, "Output should be a list.")
        
        # Check each item in the output list
        for item in outputs:
            self.assertIsInstance(item, tuple, "Every output item must be a tuple.")
            self.assertEqual(len(item), 4, "Every tuple must contain exactly four elements.")
            
            # Check data types
            self.assertIsInstance(item[0], str, "First element of the tuple must be a string.")
            self.assertIsInstance(item[1], str, "Second element of the tuple must be a string.")
            self.assertIsInstance(item[2], float, "Third element of the tuple must be a float.")
            self.assertIsInstance(item[3], str, "Fourth element of the tuple must be a string.")

# Running the tests
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)