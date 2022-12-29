#############################################################
# @file         main.py
# @author       criticalEntropy
# @date         23.12.2022
#############################################################
from btc_parser import BtcAddressMonitoring


def main():

    print("Hello World!")

    test_address = "3MCMZjWAMdGqAhi1iF1oyiiE2jY5yBAYzV"

    test_list = BtcAddressMonitoring(test_address).get_transactions_from_btc_address()

    print(test_list)
    print(len(test_list))


if __name__ == "__main__":
    main()
