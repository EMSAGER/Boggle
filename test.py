from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json



class FlaskTests(TestCase):
    def setUp(self):
        """setup before every function - no point in redundancy"""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """test the homepage's html and session"""
        ##mas testing cuando preguntas
        with self.client as client:

                    #test the route
            res = client.get("/")
            # html = res.get_data(as_text=True)

                #1. ALWAYS TEST status code first
            self.assertEqual(res.status_code, 200)
            self.assertIn('board', session)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'Timer:', res.data)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            
    def test_valid_word(self):
        """testing the check_word path by changing the session template --testing valid word"""
        with self.client as client:
            with client.session_transaction() as change:
                change['board'] = [["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"]]
        res = self.client.get('/check-word?word=cat')
            #test the res.data json results -- are we getting the correct response?
        self.assertEqual(res.json['result'], 'ok')
    
        #now repeat
    def test_invalid_word(self):
        """testing the check_word path by testing an invalid word"""
        with self.client as client:
            with client.session_transaction() as change:
                change['board'] = [["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"]]
        res = self.client.get('/check-word?word=potato')
        self.assertEqual(res.json['result'], 'not-on-board')

    def test_not_english_word(self):
        """testing the check_word path by testing a non English word"""
        with self.client as client:
            with client.session_transaction() as change:
                change['board'] = [["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"], 
                                 ["T", "A", "C", "O", "S"]]
        res = self.client.get('/check-word?word=pasdfasdfsdff')
        self.assertEqual(res.json['result'], 'not-word')
        
    def test_score(self):
        """tests the highscore pathway"""
        with self.client as client:
            data = {'score': 5}
                #This line sends a POST request to the '/score' endpoint using the Flask test client (client). It includes the JSON data (data) in the request body, which is achieved by using json.dumps(data) to serialize the dictionary into a JSON-formatted string. The content_type parameter is set to 'application/json' to indicate the type of data being sent.
            res = client.post('/score', data=json.dumps(data), content_type='application/json')
                              #After sending the request, this line retrieves the JSON response from the server using the get_json() method. It assumes that the server responds with JSON data, and result now contains the parsed JSON response.
            result = res.get_json()
            with client.session_transaction() as sess:
                highscore = sess.get('highscore')
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(highscore, 5)
            self.assertTrue(result['newRecord'])

    def test_num_plays(self):
        """tests the highscore pathway"""
        with self.client as client:
            data = {'score': 5}
                #This line sends a POST request to the '/score' endpoint using the Flask test client (client). It includes the JSON data (data) in the request body, which is achieved by using json.dumps(data) to serialize the dictionary into a JSON-formatted string. The content_type parameter is set to 'application/json' to indicate the type of data being sent.
            res = client.post('/score', data=json.dumps(data), content_type='application/json')

            
            with client.session_transaction() as sess:
                num_plays = sess.get('num_plays', 1)
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(num_plays, 1)
