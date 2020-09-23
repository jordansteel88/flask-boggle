from unittest import TestCase
from flask import session, jsonify
from app import app
from boggle import Boggle


class BoggleTests(TestCase):

    def setUp(self):
        """Pretest setup."""

        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_home(self):
        """Check session variables and HTML display"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('record'))
            self.assertIsNone(session.get('plays'))
            self.assertIn(b'<p id="message"></p>', response.data)


    def test_handle_guess(self):
        """Test word validity response on a session board"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['W', 'O', 'R', 'D', 'S'],
                                 ['W', 'O', 'R', 'D', 'S'],
                                 ['W', 'O', 'R', 'D', 'S'],
                                 ['W', 'O', 'R', 'D', 'S'],
                                 ['W', 'O', 'R', 'D', 'S'],]
        
        res = self.client.get('/submit-guess?guess=word')  
        self.assertEqual(res.json['result'], 'ok')  

        not_on_board_res = self.client.get('/submit-guess?guess=cat')
        self.assertEqual(not_on_board_res.json['result'], 'not-on-board')         
        
        not_word_res = self.client.get('/submit-guess?guess=qwertyuiop')
        self.assertEqual(not_word_res.json['result'], 'not-word')  


    def test_track_score(self):
        """Check record logic"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['record'] = 5

        data = {'score': 10}
        res = self.client.post('/track-score', json = data, content_type='application/json')
        self.assertTrue(res.json['newRecord'])




