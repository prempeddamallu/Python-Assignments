import unittest
from flask import json
from app import app  # Import the Flask app from app.py

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_greet_default(self):
        response = self.app.get('/api/greet')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['message'], 'Hello, World!')

    def test_greet_with_name(self):
        response = self.app.get('/api/greet?name=Alice')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['message'], 'Hello, Alice!')

if __name__ == '__main__':
    unittest.main()
