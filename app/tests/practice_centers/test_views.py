import unittest

from app.tests.test_basic_views import BasicViewTests


class PracticeCentersViewsTests(BasicViewTests):

    def test_practice_centers_with_no_practice_center_should_display_no_practice_center(self):
        self.remove_practice_centers()
        response = self.app.get('/practice-centers', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SportsApp', response.data)
        self.assertIn(b'Practice Centers', response.data)
        self.assertNotIn(b'Mont-Orford National Park', response.data)
        self.assertNotIn(b'Parc des Montagnards', response.data)
        self.assertNotIn(b'Gault Nature Reserve of McGill University', response.data)

    def test_practice_centers_with_practice_centers_should_display_practice_centers(self):
        response = self.app.get('/practice-centers', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SportsApp', response.data)
        self.assertIn(b'Practice Centers', response.data)
        self.assertIn(b'Mont-Orford National Park', response.data)
        self.assertIn(b'Parc des Montagnards', response.data)
        self.assertIn(b'Gault Nature Reserve of McGill University', response.data)

    def test_practice_centers_with_form_should_display_filtered_practice_centers(self):
        response = self.app.post('/practice-centers', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SportsApp', response.data)
        self.assertIn(b'Practice Centers', response.data)
        self.assertIn(b'Mont-Orford National Park', response.data)
        self.assertNotIn(b'Parc des Montagnards', response.data)
        self.assertNotIn(b'Gault Nature Reserve of McGill University', response.data)

    def test_practice_center_details_should_display_practice_center_details(self):
        response = self.app.get('/practice-centers/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mont-Orford National Park', response.data)
        response = self.app.get('/practice-centers/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Parc des Montagnards', response.data)
        response = self.app.get('/practice-centers/3', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gault Nature Reserve of McGill University', response.data)

    def test_practice_center_details__without_practice_center_should_respond_not_found(self):
        self.remove_practice_centers()
        response = self.app.get('/practice-centers/1', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Not Found', response.data)


if __name__ == "__main__":
    unittest.main()