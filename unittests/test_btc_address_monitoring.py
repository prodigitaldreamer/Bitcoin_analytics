#############################################################
# @file     test_btc_address_monitoring.py
# @author   criticalEntropy
# @date     23.12.2022
#############################################################

import unittest
from unittest.mock import patch

from btc_parser import BtcAddressMonitoring
import requests

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

    def setUp(self):
        # Set up test data and mock objects as needed
        self.watch_address = "3MCMZjWAMdGqAhi1iF1oyiiE2jY5yBAYzV"
        self.transaction_list = []
        self.mock_response = {
            "txs": [
                {
                    "inputs": [
                        {
                            "prev_out": {
                                "addr": "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX"
                            }
                        }
                    ],
                    "out": [
                        {
                            "addr": "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX",
                            "value": 1000000
                        }
                    ]
                },
                {
                    "inputs": [
                        {
                            "prev_out": {
                                "addr": "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX"
                            }
                        }
                    ],
                    "out": [
                        {
                            "addr": "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX",
                            "value": 2000000
                        }
                    ]
                }
            ],
            "n_tx": 2
        }

    @patch("requests.get")
    def test_get_transactions_success(self, mock_get):
        # Test the function when the API request is successful
        mock_get.return_value.json.return_value = self.mock_response
        mock_get.return_value.raise_for_status.return_value = None
        expected_result = [
            ("1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX", "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX", 1000000),
            ("1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX", "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX", 2000000)
        ]

        # Call the function being tested
        result = test_monitor.get_transactions_from_btc_address()

        # Assert that the function returns the expected result
        self.assertEqual(result, expected_result)

    @patch("requests.get")
    def test_get_transactions_api_error(self, mock_get):
        # Test the function when the API request returns an error
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.RequestException
        expected_result = []

        # Call the function being tested
        result = test_monitor.get_transactions_from_btc_address()

        # Assert that the function returns an empty list when the API request fails
        self.assertEqual(result, expected_result)

    @patch("requests.get")
    def test_get_transactions_invalid_data(self, mock_get):
        # Test the function when the API response contains transactions without input or output addresses or amounts
        mock_response = {
            "txs": [
                {
                    "inputs": [
                        {
                            "prev_out": {
                                "addr": "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX"
                            }
                        }
                    ],
                    "out": []
                },
                {
                    "inputs": [],
                    "out": [
                        {
                            "addr": "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX",
                            "value": 2000000
                        }
                    ]
                },
                {
                    "inputs": [
                        {
                            "prev_out": {
                                "addr": "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX"
                            }
                        }
                    ],
                    "out": [
                        {
                            "addr": "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX"
                        }
                    ]
                }
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status.return_value = None
        expected_result = []

        # Call the function being tested
        result = test_monitor.get_transactions_from_btc_address()

        # Assert that the function returns the expected result
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
