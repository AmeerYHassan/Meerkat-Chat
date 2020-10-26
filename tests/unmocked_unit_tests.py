# pylint: disable=C0114, E0401, C0413, C0115, C0116
# C0114, C0116 disabled because docstrings are not needed to understand tests here.
# E0401, C0413 state app is not being imported, but it is.

from datetime import datetime
import unittest
import sys

sys.path.append("..")
import app

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                "KEY_INPUT": "!!help",
                "KEY_EXPECTED": "!!funtranslate <message> to translate a message to yoda speech, "\
                                "!!time to get the current time, "\
                                "!!catfact to get a random cat fact, "\
                                "!!giphy <query> to retrieve a gif, "\
                                "or !!about to learn a bit more about me"
            },
            {
                "KEY_INPUT": "!!about",
                "KEY_EXPECTED": "Hi, I'm meerkat, and I'm just a small utility "\
                                "for this chat room! Use !!help to see what I can do!"
            },
            {
                "KEY_INPUT": "!!AAAAAA",
                "KEY_EXPECTED": "Sorry, I don't know that command. Use !!help to see what I can do!"
            },
            {
                "KEY_INPUT": "!about",
                "KEY_EXPECTED": "Hi, I'm meerkat, and I'm just a small utility "\
                                "for this chat room! Use !!help to see what I can do!"
            },
            {
                "KEY_INPUT": "!!time",
                "KEY_EXPECTED": "The current time is " + datetime.now().strftime("%H:%M:%S")
            },
            {
                "KEY_INPUT": "!!funtranslate hello, this is a test "\
                             "to trying to get output for me to make a test case",
                "KEY_EXPECTED": "Sorry, I only can translate sentences "\
                                "that just contain letters! Try again"
            }
        ]

        self.failure_test_params = [
            {
                "KEY_INPUT": "!!about",
                "KEY_EXPECTED": "!!funtranslate <message> to translate a message to yoda speech, "\
                                "!!time to get the current time, "\
                                "!!catfact to get a random cat fact, "\
                                "!!giphy <query> to retrieve a gif, "\
                                "or !!about to learn a bit more about me"
            },
            {
                "KEY_INPUT": "!!help",
                "KEY_EXPECTED": "Hi, I'm meerkat, and I'm just a small utility for this chat room!"\
                                "Use !!help to see what I can do!"
            },
            {
                "KEY_INPUT": "!!abot",
                "KEY_EXPECTED": "Hi, I'm meerkat, and I'm just a small utility for this chat room!"\
                                "Use !!help to see what I can do!"
            },
            {
                "KEY_INPUT": "!!h",
                "KEY_EXPECTED": "!!funtranslate <message> to translate a message to yoda speech, "\
                                "!!time to get the current time, "\
                                "!!catfact to get a random cat fact, "\
                                "!!giphy <query> to retrieve a gif, "\
                                "or !!about to learn a bit more about me"
            }
        ]


    def test_bot_response_success(self):
        for test in self.success_test_params:
            response = app.getBotResponse({}, test["KEY_INPUT"])["message"]
            expected = test["KEY_EXPECTED"]
            self.assertEqual(response, expected)

    def test_parse_message_failure(self):
        for test in self.failure_test_params:
            response = app.getBotResponse({}, test["KEY_INPUT"])["message"]
            expected = test["KEY_EXPECTED"]
            self.assertNotEqual(response, expected)

if __name__ == '__main__':
    unittest.main()
