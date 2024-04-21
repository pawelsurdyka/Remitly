import unittest
from unittest.mock import mock_open, patch
from check_resources import check

class TestCheckFunction(unittest.TestCase):
    # JSON file {}
    def test_empty_file(self):
        with patch("builtins.open", mock_open(read_data="{}")) as mock_file:
            result = check("example.json")
            self.assertEqual(result, "Plik JSON jest pusty.")

    # JSON file {"PolicyName": "root","PolicyDocument": {"Version": "2012-10-17"}}
    def test_missing_statement_key(self):
        with patch("builtins.open", mock_open(read_data='{"PolicyName": "root","PolicyDocument": '
                                                        '{"Version": "2012-10-17"}}')) as mock_file:
            result = check("example.json")
            self.assertEqual(result, "Brak instrukcji (Statement) w pliku JSON.")

    # JSON file {"PolicyName": "root","PolicyDocument": {"Version": "2012-10-17", "Statement": [{}]}}
    def test_missing_resource_key(self):
        with (patch("builtins.open", mock_open(read_data='{"PolicyName": "root","PolicyDocument": '
                                                        '{"Version": "2012-10-17", "Statement": [{}]}}'))
              as mock_file):
            result = check("example.json")
            self.assertEqual(result, "Klucz 'Resource' nie został znaleziony w pierwszej instrukcji.")

    # JSON file {"PolicyName": "root","PolicyDocument": {"Version": "2012-10-17", "Statement": [{"Resource": "*"}]}}
    def test_resource_all(self):
        with (patch("builtins.open", mock_open(read_data='{"PolicyName": "root","PolicyDocument": '
                                                        '{"Version": "2012-10-17", "Statement": [{"Resource": "*"}]}}'))
              as mock_file):
            result = check("example.json")
            self.assertEqual(result, False)

    # JSON file {"PolicyName": "root","PolicyDocument": {"Version": "2012-10-17", "Statement": '[{"Resource": "arn:aws:s3:::example-bucket"}]}}
    def test_valid_resource(self):
        with (patch("builtins.open", mock_open(read_data='{"PolicyName": "root","PolicyDocument": '
                                                        '{"Version": "2012-10-17", "Statement": '
                                                        '[{"Resource": "arn:aws:s3:::example-bucket"}]}}'))
              as mock_file):
            result = check("example.json")
            self.assertEqual(result, True)

    # JSON file
    def test_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = check("non_existent_file.json")
            self.assertEqual(result, "Plik nie został znaleziony.")

    # JSON file {"invalid_json"
    def test_invalid_json_format(self):
        with patch("builtins.open", mock_open(read_data='{"invalid_json"')) as mock_file:
            result = check("example.json")
            self.assertEqual(result, "Błąd dekodowania JSON. Plik JSON ma niepoprawny format.")

if __name__ == '__main__':
    unittest.main()
