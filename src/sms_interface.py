#############################################################
# @file     sms_interface.py
# @author   criticalEntropy
# @date     30.12.2022
# Hints:    https://developer.vonage.com/messaging/sms/overview
#############################################################
import os
from nexmo import Client


class SmsHandling:
    # Constructor
    def __init__(self, from_number, to_number, message_text):
        self.from_number = from_number
        self.to_number = to_number
        self.message_text = message_text

    # Destructor
    def __del__(self):
        print(f"Deleting SmsHandling object")

    #############################################################
    # @brief    This function sends an SMS from a mobile number to a mobile number with a defined text.
    #           Note that admin rights are required to read the environment variables for API access.
    #           Also note that a user account with VONAGE API (formerly NEXMO) is required to define
    #           Key and Secret for the value of the environment variable.
    #
    # @para     from_number - Cell phone number from which the SMS should be sent
    # @para     to_number - Cell phone  to which the SMS should be sent
    # @para     message_text - Message to be sent
    # @return   true/false
    # @author   criticalEntropy
    # @date     30.12.2022
    #############################################################
    def send_sms_via_nexmo(self):
        try:
            # Replace with your Twilio account SID and auth token
            api_key = os.environ['NEXMO_API_KEY']
            api_secret = os.environ['NEXMO_API_SECRET']

            # Create a Nexmo client
            client = Client(key=api_key, secret=api_secret)

            # Send the SMS
            response = client.send_message({
                'from': self.from_number,
                'to': self.to_number,
                'text': self.message_text
            })
            print(f"Sent message to number {response}")
            return True
        except Exception as err:
            # Handle any errors that occur
            print(f"An error occurred: {err}")
            return False
