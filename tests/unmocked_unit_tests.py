import unittest
import sys

sys.path.append("..")
import app

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                "KEY_INPUT": "!!help",
                "KEY_EXPECTED": {
                    "KEY_IS_BOT": True,
                    "KEY_BOT_COMMAND": "help",
                    "KEY_MESSAGE": "",
                }
            },
        ]
        
        self.failure_test_params = [
            # TODO HW13
        ]


    def bot_response_success(self):
        for test in self.success_test_params:
            response = app.getBotResponse(test["KEY_INPUT"])
            expected = test["KEY_EXPECTED"]
            
            # self.assertEqual(response[KEY_IS_BOT], expected[KEY_IS_BOT])
            
    def test_parse_message_failure(self):
        for test in self.failure_test_params:
            response = app.getBotResponse(test["KEY_INPUT"])
            expected = test["KEY_EXPECTED"]
            
            # TODO add assertNotEqual cases here instead

if __name__ == '__main__':
    unittest.main()