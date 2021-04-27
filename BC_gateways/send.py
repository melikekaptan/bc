#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from crypto import Crypto
from encoders import transaction_encode
from utils import text_to_bytes
from network import Network
from unconfirmed_transactions_loader import UnconfirmedPaymentsLoader
from transaction_helper import build_transaction

import re
import logging

ADDRESS_PATTERN = re.compile('^[a-f0-9]{64}$')

class SendCommand:
    

    def __init__(self, *args):
        if len(args) != 3:
            logging.error('wrong number of args for {}'.format(SendCommand))

        else:
            from_gateway_or_key = args[0]
            ipfs_doc_txt = args[1]
            model = args[2]

            crypto = Crypto()
            key = crypto.get_key(from_gateway_or_key) or crypto.get_key_by_address(from_gateway_or_key)
            logging.info('from_gateway key get')

            if not key:
                logging.error('invalid from address/key')

            #elif not (crypto.get_key(to_address_or_key) or self._is_valid_address_format(to_address_or_key)):
             #   logging.error('invalid to address/key')

#            elif not self._is_valid_ipfs_doc_format(ipfs_doc_txt):
 #               logging.error('invalid ipfs_doc')

            else:
                    transaction = build_transaction(key.address, ipfs_doc_txt, model, key)
                    logging.info('transaction built')
                    SendCommand.send_transaction(transaction)

    @staticmethod
    def send_transaction(transaction):
        encoded_transaction_text = transaction_encode(transaction)
        encoded_transaction_bytes = text_to_bytes(encoded_transaction_text)

        Network().send_transaction(encoded_transaction_bytes)

    def _is_valid_address_format(self, address_candidate):
        return ADDRESS_PATTERN.match(address_candidate)

    def _is_valid_ipfs_doc_format(self, ipfs_doc_txt):
        try:
            return float(ipfs_doc_txt) > 0
        except ValueError:
            return False
        
        
SendCommand('GWWWWw', 'A7937B64B8CAA58F03721BB6BACF5C78CB235FEBE0E70B1B84CD99541461A08E', '12345678')
SendCommand('GWWWWW', '16367AACB67A4A017C8DA8AB95682CCB390863780F7114DDA0A0E0C55644C7C4', '23456789')
        

