import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_api_route(self):
        response = self.app.get('/api')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_rezultate_route(self):
        response = self.app.post('/api/rezultate', data={'link': 'done', 'id': '1', 'subiect': 'math'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_creare_route(self):
        response = self.app.get('/creare')
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_events_route(self):
        response = self.app.get('/events')
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_see_contents_route(self):
        response = self.app.get('/events/event_202201011200')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html')

    def test_download_file_route(self):
        response = self.app.get('/events/event_202201011200/file.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/plain')

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html')

    def test_register_route(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html')

    def test_punctaje_route(self):
        response = self.app.get('/punctaje')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html')

    def test_logout_route(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)  # Redirect to login page

if __name__ == '__main__':
    unittest.main()