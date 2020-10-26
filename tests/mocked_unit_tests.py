# pylint: disable=C0116, C0115, C0114, W0613, R0903, E0401, C0413
# C0116, C0114, C0115 disabled since docstrings are not necessary to understand functions here
# W0613 disabled because link is mandatory to be passed in, even though it is not used.
# R0903 disabled because not many class methods are needed
# E0401, C0413 state that app is not being imported, but it is being imported correctly.

from unittest import mock
import unittest
import sys

from os.path import dirname, join
sys.path.insert(1, join(dirname(__file__), '../'))

import app

class MockedResponse:
    def __init__(self, status_code, json):
        self.status_code = status_code
        self.json_dict = json

    def json(self):
        return self.json_dict

def return_valid_cat_fact(link):
    curr_cat = MockedResponse(200, {"fact":"Cats have four legs!"})
    return curr_cat

def return_invalid_cat_fact(link):
    curr_cat = MockedResponse(404, {"fact":"blabla"})
    return curr_cat

def return_valid_funtranslate(link):
    curr_translation = MockedResponse(200,
        {'contents':
            {'translated': \
                'A test to trying to get output for me to make a test case,  '\
                'Force be with you this is'}
        })
    return curr_translation

def return_valid_funtranslate_with_special_characters(link):
    curr_translation = MockedResponse(200, {'contents': {'translated': 'filler text'}})
    return curr_translation

def return_invalid_funtranslate(link):
    curr_translation = MockedResponse(404, {'contents': {'translated': 'filler text'}})
    return curr_translation

def return_valid_gif(link):
    curr_gif = MockedResponse(200,
        {'data': [{'images': {'original': {'url': 'https://mock.url/'}}}]})
    return curr_gif

def return_invalid_gif(link):
    curr_gif = MockedResponse(404,
        {'data': [{'images': {'original': {'url': 'https://mock.url/'}}}]})
    return curr_gif

class ChatbotTestCase(unittest.TestCase):
    def test_valid_cat_fact(self):
        with mock.patch('app.requests.get', return_valid_cat_fact):
            response = app.getBotResponse({}, "!!catfact")["message"]
            expected = "Cats have four legs!"
            self.assertEqual(response, expected)

    def test_invalid_cat_fact(self):
        with mock.patch('app.requests.get', return_invalid_cat_fact):
            response = app.getBotResponse({}, "!!catfact")["message"]
            expected = "Uh oh! Try again in a few, I can't seem to get a cat fact right now."
            self.assertEqual(response, expected)

    def test_valid_translation(self):
        with mock.patch('app.requests.get', return_valid_funtranslate):
            response = app.getBotResponse({}, "!!funtranslate filler")["message"]
            expected = \
                "A test to trying to get output for me to make a test case,"\
                "  Force be with you this is"
            self.assertEqual(response, expected)

    def test_invalid_translation(self):
        with mock.patch('app.requests.get', return_invalid_funtranslate):
            response = app.getBotResponse({}, "!!funtranslate filler")["message"]
            expected = "Uh oh! Try again in a few, I can't seem to translate that right now."
            self.assertEqual(response, expected)

    def test_valid_translation_with_specials(self):
        with mock.patch('app.requests.get', return_valid_funtranslate_with_special_characters):
            response = app.getBotResponse({}, "!!funtranslate this isn't correct!")["message"]
            expected = "Sorry, I only can translate sentences that just contain letters! Try again"
            self.assertEqual(response, expected)

    def test_valid_gif(self):
        with mock.patch('app.requests.get', return_valid_gif):
            response = app.getBotResponse({}, "!!giphy test")["imageLink"]
            expected = 'https://mock.url/'
            self.assertEqual(response, expected)

    def test_invalid_gif(self):
        with mock.patch('app.requests.get', return_invalid_gif):
            response = app.getBotResponse({}, "!!giphy test")["message"]
            expected = "Uh oh! Try again in a few, I can't seem to get a gif right now."
            self.assertEqual(response, expected)

    def test_no_gif_returned(self):
        with mock.patch('app.requests.get', return_valid_gif):
            response = app.getBotResponse({}, "!!giphy test")["imageLink"]
            expected = "Uh oh! Try again in a few, I can't seem to get a gif right now."
            self.assertNotEqual(response, expected)

    def test_valid_translation_with_specials_false(self):
        with mock.patch('app.requests.get', return_valid_funtranslate_with_special_characters):
            response = app.getBotResponse({}, "!!funtranslate this isn't correct!")["message"]
            expected = \
                "A test to trying to get output for me to make a test case, "\
                " Force be with you this is"
            self.assertNotEqual(response, expected)

    def test_valid_cat_fact_false(self):
        with mock.patch('app.requests.get', return_valid_cat_fact):
            response = app.getBotResponse({}, "!!catfact")["message"]
            expected = "Uh oh! Try again in a few, I can't seem to get a cat fact right now."
            self.assertNotEqual(response, expected)

if __name__ == '__main__':
    unittest.main()
