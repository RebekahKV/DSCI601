import unittest
import json

class TestJsonDataFormat(unittest.TestCase):
    def test_is_list(self):
        """Test if the content of the JSON file is a list."""
        try:
            with open('Delhi.json', 'r') as file:
                data = json.load(file)
            # Check if data is a list
            self.assertIsInstance(data, list, "The root of the JSON file should be a list.")
        except FileNotFoundError:
            self.fail("The JSON file was not found.")
        except json.JSONDecodeError:
            self.fail("JSON file is not properly formatted.")

# Running the test
if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)