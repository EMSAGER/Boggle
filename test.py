from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

class FlaskTests(TestCase):
    def setUp(self):
        """setup before every function - no point in redundancy"""
        self.client = app.test_client()
    # TODO -- write tests for every view function / feature!

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

    def test_not_word(self):
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
        