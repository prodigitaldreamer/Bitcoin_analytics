#############################################################
# @file     test_btc_address_monitoring.py
# @author   criticalEntropy
# @date     23.12.2022
#############################################################

import unittest
from unittest.mock import patch

from btc_parser import BtcAddressMonitoring

# Create an instance of the BtcAddressMonitoring class
test_monitor = BtcAddressMonitoring('watch_address')

class TestBtcAddressMonitoring(unittest.TestCase):
    @patch('requests.get')
    def test_is_tx_transaction_from_btc_address(self, mock_get):
        # Set up the mock response to return a JSON dictionary with a transaction
        # where the watchAddress sends BTC
        mock_get.return_value.json.return_value = {
            'txs': [{
                'inputs': [{
                    'prev_out': {
                        'addr': 'watch_address'
                    }
                }]
            }]
        }

        # Call the function with the watchAddress
        result = test_monitor.is_tx_transaction_from_btc_address()

        # Assert that the function returns True
        self.assertTrue(result)

    @patch('requests.get')
    def test_is_rx_transaction_to_btc_address(self, mock_get):
        # Set up the mock response to return a JSON dictionary with a transaction
        # where the watchAddress receives BTC
        mock_get.return_value.json.return_value = {
            'txs': [{
                'out': [{
                    'addr': 'watch_address'
                }]
            }]
        }

        # Call the function with the watchAddress
        result = test_monitor.is_rx_transaction_to_btc_address()

        # Assert that the function returns True
        self.assertTrue(result)

    @patch('requests.get')
    def test_does_not_send_or_receive_btc(self, mock_get):
        # Set up the mock response to return a JSON dictionary with a transaction
        # where the watchAddress does not send or receive BTC
        mock_get.return_value.json.return_value = {
            'txs': [{
                'inputs': [{
                    'prev_out': {
                        'addr': 'other_address'
                    }
                }],
                'out': [{
                    'addr': 'other_address'
                }]
            }]
        }

        # Call the functions with the watchAddress
        tx_result = test_monitor.is_tx_transaction_from_btc_address()
        rx_result = test_monitor.is_rx_transaction_to_btc_address()

        # Assert that the functions return False
        self.assertFalse(tx_result)
        self.assertFalse(rx_result)

    @patch('requests.get')
    def test_api_error(self, mock_get):
        # Set up the mock to raise an exception when called
        mock_get.side_effect = Exception

        # Call the functions with the watchAddress, catching the exception if it is raised
        try:
            tx_result = test_monitor.is_tx_transaction_from_btc_address()
        except Exception:
            tx_result = False
        try:
            rx_result = test_monitor.is_rx_transaction_to_btc_address()
        except Exception:
            rx_result = False

        # Assert that the functions return False when an exception is raised
        self.assertFalse(tx_result)
        self.assertFalse(rx_result)


if __name__ == '__main__':
    unittest.main()
