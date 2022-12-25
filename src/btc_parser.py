#############################################################
# @file     btc_parser.py
# @author    criticalEntropy
# @date     23.12.2022
#############################################################

# Import packages
import requests


class BtcAddressMonitoring:
    # Constructor
    def __init__(self, watch_address):
        self.watch_address = watch_address

    # Destructor
    def __del__(self):
        print(f"Deleting BtcAddressMonitoring object with watch_address {self.watch_address}")

    #############################################################
    # @brief    This function monitors a bitcoin address and returns 'True' in
    #           case of an unconfirmed Tx-transaction.
    #           The function returns 'False' if no btc was sent from the address.
    #           An unconfirmed transaction is cached in the memory pool.
    #           This function needs to be run periodically to monitor new unconfirmed transactions.
    #           For example, you could set up a cron job that runs the script every 5 minutes.
    #
    # @para     watch_address - Address to be monitored
    # @return   boolean - BTC sent from monitored address?
    # @author   criticalEntropy
    # @date     23.12.2022
    #############################################################
    def is_tx_transaction_from_btc_address(self):
        # Send an HTTP request to the Blockchain.info API to retrieve the list of unconfirmed transactions
        api_url = 'https://blockchain.info/unconfirmed-transactions?format=json'

        # Make sure that the API call was successful and no HTTP errors occurred
        try:
            response = requests.get(api_url)
            response.raise_for_status()
        except (requests.exceptions.RequestException, ValueError) as err:
            print(f"An error occurred while trying to retrieve the list of unconfirmed transactions: {err}")
            return False

        # Make sure that the response of the API call could be parsed correctly
        try:
            # Parse the response as a JSON dictionary
            unconfirmed_transactions = response.json()
        except ValueError as err:
            print(f"An error occurred while parsing the response as a JSON dictionary: {err}")
            return False

        # Make sure that the API response object has the expected format and that the required keys are present.
        try:
            # Iterate over each unconfirmed transaction
            for transaction in unconfirmed_transactions['txs']:
                # Check if the address to be monitored has sent bitcoin
                if transaction['inputs'][0]['prev_out']['addr'] == self.watch_address:
                    # BTC was sent
                    return True
        except (KeyError, IndexError) as err:
            print("An error occurred while parsing the API response:", err)
            return False

        # Return False if the monitored address has not sent any BTC
        return False

    #############################################################
    # @brief    This function monitors a bitcoin address and returns 'True' in
    #           case of an unconfirmed Rx-transaction.
    #           The function returns 'False' if no btc was received from the address.
    #           An unconfirmed transaction is cached in the memory pool.
    #           This function needs to be run periodically to monitor new unconfirmed transactions.
    #           For example, you could set up a cron job that runs the script every 5 minutes.
    #
    # @para     watch_address - Address to be monitored
    # @return   boolean - BTC received by monitored address?
    # @author   criticalEntropy
    # @date     23.12.2022
    #############################################################
    def is_rx_transaction_to_btc_address(self):
        # Send an HTTP request to the Blockchain.info API to retrieve the list of unconfirmed transactions
        api_url = 'https://blockchain.info/unconfirmed-transactions?format=json'

        # Make sure that the API call was successful and no HTTP errors occurred
        try:
            response = requests.get(api_url)
            response.raise_for_status()
        except (requests.exceptions.RequestException, ValueError) as err:
            print(f"An error occurred while trying to retrieve the list of unconfirmed transactions: {err}")
            return False

        # Make sure that the response of the API call could be parsed correctly.
        try:
            # Parse the response as a JSON dictionary
            unconfirmed_transactions = response.json()
        except ValueError as err:
            print(f"An error occurred while parsing the response as a JSON dictionary: {err}")
            return False

        # Make sure that the response of the API call could be parsed correctly
        try:
            # Iterate over each unconfirmed transaction
            for transaction in unconfirmed_transactions['txs']:
                for output in transaction['out']:
                    # Check if the address to be monitored has received bitcoin
                    if 'addr' in output and output['addr'] == self.watch_address:
                        # BTC received
                        return True
        except (KeyError, IndexError) as err:
            print("An error occurred while parsing the API response:", err)
            return False

        # Return False if the monitored address has not received any BTC
        return False
