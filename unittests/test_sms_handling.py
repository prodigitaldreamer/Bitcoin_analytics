#############################################################
# @file     test_sms_handling.py
# @author   criticalEntropy
# @date     30.12.2022
# Hint:     Check if the script is running as an administrator
#           This is important because in case of no admin rights the environment variables for API access cannot be read
#           It should be noted that this code works for a Windows machine
#############################################################

import unittest
from unittest.mock import patch
from sms_interface import SmsHandling
import ctypes
import sys


class TestSmsHandling(unittest.TestCase):

    def setUp(self):
        # Set up test case
        self.from_number = "+1234567890"
        self.to_number = "+0987654321"
        self.message_text = "Test message"

    def test_send_sms(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            # Restart the script with administrator privileges
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        else:
            self.setUp()
            sms_handler = SmsHandling(self.from_number, self.to_number, self.message_text)

            # Patch client.send_message to return a mock response
            with patch("sms_interface.Client.send_message") as mock_send_message:
                mock_send_message.return_value = {'message-count': '1', 'messages': [
                    {'to': self.to_number, 'message-id': '0C0000007F3D3D3F', 'status': '0', 'remaining-balance': '0.0',
                     'message-price': '0.00300000', 'network': '23410'}]}
                result = sms_handler.send_sms_via_nexmo()

            # Assert that the method returned True and that send_message was called with the correct arguments
            self.assertTrue(result, f"send_sms_via_nexmo() returned {result}, expected True")
            mock_send_message.assert_called_with({'from': self.from_number, 'to': self.to_number,
                                                  'text': self.message_text})

    def test_send_sms_failure(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            # Restart the script with administrator privileges
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        else:
            self.setUp()
            sms_handler = SmsHandling(self.from_number, self.to_number, self.message_text)

            # Patch client.send_message to raise an exception
            with patch("sms_interface.Client.send_message") as mock_send_message:
                mock_send_message.side_effect = Exception("Error sending SMS")
                result = sms_handler.send_sms_via_nexmo()

            # Assert that the method returned False and that send_message was called with the correct arguments
            self.assertFalse(result, f"send_sms_via_nexmo() returned {result}, expected False")


if __name__ == '__main__':
    unittest.main()
