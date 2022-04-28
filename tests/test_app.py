import unittest
from urllib import response

from dotenv import load_dotenv
load_dotenv()

from openWeatherFlask.app import app

class TestGetCitiesTemperatures(unittest.TestCase):

    def test_london(self):
        """Test get london temperatures"""
        test_client = app.test_client()
        response = test_client.get('/london')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'London' in response.data)
    
    def test_ituiutaba(self):
        """Test get uberlandia temperatures"""
        test_client = app.test_client()
        response = test_client.get('/ituiutaba')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Ituiutaba' in response.data)
    
    def test_natal(self):
        """Test get natal temperatures"""
        test_client = app.test_client()
        response = test_client.get('/natal')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Natal' in response.data)
    
    def test_not_founded_city(self):
        """Test get not founded city error"""
        test_client = app.test_client()
        response = test_client.get('/not_founded_city')

        self.assertEqual(response.status_code, 404)
        self.assertTrue(b'city not found' in response.data)

    def test_cached_cities_empty(self):
        """Test get cached cities temperatures"""
        test_client = app.test_client()
        response = test_client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'cities_cached' : []})
    
    def test_zcached_cities(self):
        """Test get cached cities temperatures"""
        test_client = app.test_client()
        response = test_client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue( b'Natal' in response.data)