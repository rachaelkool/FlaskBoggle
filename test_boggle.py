from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    def test_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('no_plays'))

    def test_invalid(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "U", "T", "E", "O"], 
                                 ["C", "A", "T", "G", "O"], 
                                 ["C", "A", "T", "T", "M"], 
                                 ["Z", "Z", "P", "T", "L"], 
                                 ["C", "A", "T", "B", "L"]]
            resp = client.get('/check-word?word=elephant')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-on-board')


    def test_valid(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "U", "T", "E", "O"], 
                                 ["C", "A", "T", "G", "O"], 
                                 ["C", "A", "T", "T", "M"], 
                                 ["Z", "Z", "P", "T", "L"], 
                                 ["C", "A", "T", "B", "L"]]
            resp = client.get('/check-word?word=cute')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'ok')


    def test_nonenglish(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "U", "T", "E", "O"], 
                                 ["C", "A", "T", "G", "O"], 
                                 ["C", "A", "T", "T", "M"], 
                                 ["Z", "Z", "P", "T", "L"], 
                                 ["C", "A", "T", "B", "L"]]
            resp = client.get('/check-word?word=dhfhihdih')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-word')



