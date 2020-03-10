import os
import unittest

from app import app, conn
from app.models import Sport
from app.queries import SportQuery
from app.tests.test_db_create import test_db_create


class SportsTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['MYSQL_BD'] = 'test'

        self.app = app.test_client()

        test_db_create()

        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass

    def add_sports(self):
        sport1 = Sport(None, name='Randonnee')
        sport2 = Sport(None, name='Escalade')
        sport3 = Sport(None, name='Natation')
        SportQuery().add(sport1)
        SportQuery().add(sport2)
        SportQuery().add(sport3)

    def test_sports_with_no_sport_should_display_no_sport(self):
        response = self.app.get('/sports/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SportsApp', response.data)
        self.assertIn(b'Sports', response.data)
        self.assertNotIn(b'Randonnee', response.data)
        self.assertNotIn(b'Escalade', response.data)
        self.assertNotIn(b'Natation', response.data)

    def test_sports_with_sports_should_display_sports(self):
        self.add_sports()
        response = self.app.get('/sports/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SportsApp', response.data)
        self.assertIn(b'Sports', response.data)
        self.assertIn(b'Randonnee', response.data)
        self.assertIn(b'Escalade', response.data)
        self.assertIn(b'Natation', response.data)

    def test_sport_details_should_display_sport_details(self):
        self.add_sports()
        response = self.app.get('/sports/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Randonnee', response.data)
        response = self.app.get('/sports/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Escalade', response.data)
        response = self.app.get('/sports/3', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Natation', response.data)

    def test_sport_details__without_sport_should_display_not_found(self):
        response = self.app.get('/sports/1', follow_redirects=True)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
