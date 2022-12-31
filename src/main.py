#############################################################
# @file         main.py
# @author       criticalEntropy
# @date         30.12.2022
#############################################################
import sys
import ctypes
import time
from sms_interface import SmsHandling
from btc_parser import BtcAddressMonitoring

# Define Constants
CHECK_INTERVAL_SECONDS = 30
SATOSHI_FIRST_ADDRESS = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
OWN_PHONE_NUMBER = '+4912345678900'
SMS_MESSAGE_TEXT = 'Attention, Satoshi has made a transaction!'


def main():
    transaction_occurred = False

    # Check if the script is running as an administrator
    # This is important because in case of no admin rights the environment variables for API access cannot be read
    # It should be noted that this code works for a Windows machine
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # Restart the script with administrator privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        # Check the memory pool as long as no transaction was sent from the genesis address
        while not transaction_occurred:
            # Check the memory pool every CHECK_INTERVAL_SECONDS seconds
            time.sleep(CHECK_INTERVAL_SECONDS)
            try:
                # Check if a transaction was sent from the address to be monitored
                transaction_occurred = BtcAddressMonitoring(SATOSHI_FIRST_ADDRESS).is_tx_transaction_from_btc_address()
            except Exception as err:
                # Handle any exceptions that may occur
                print('An error occurred while checking the BTC address transaction status:', err)

        # When the loop is exited, a transaction was sent from the address to be monitored.
        # In this case an SMS should be sent
        try:
            SmsHandling(OWN_PHONE_NUMBER, OWN_PHONE_NUMBER, SMS_MESSAGE_TEXT).send_sms_via_nexmo()
        except Exception as err:
            # Handle any exceptions that may occur
            print('An error occurred while sending the SMS:', err)


if __name__ == "__main__":
    main()
