#!/usr/bin/env python3

from crypto import Crypto
from encoders import transaction_encode
from utils import text_to_bytes
from network import Network
from unconfirmed_transactions_loader import UnconfirmedPaymentsLoader
from transaction_helper import build_transaction
from listen_and_list_active_gateways import GatewayListener
from threading import Event
import re
import logging
import signal, sys
import time 

ADDRESS_PATTERN = re.compile('^[a-f0-9]{64}$')

class SendCommand:
    

    def __init__(self, *args):
        if len(args) != 3:
            logging.error('wrong number of args for {}'.format(SendCommand))

        else:
            from_address_or_key = args[0]
            ipfs_doc_txt = args[1]
            model = args[2]

            crypto = Crypto()
            key = crypto.get_key(from_address_or_key) or crypto.get_key_by_address(from_address_or_key)
            logging.info('from_address key get')

            if not key:
                logging.error('invalid from address/key')

                transaction = build_transaction(key.address, ipfs_doc_txt, model, key)
                logging.info('transaction built')
                UnconfirmedPaymentsLoader().process(lambda u_p : u_p.add(transaction))

                SendCommand.send_transaction(transaction)
        

    @staticmethod
    def send_transaction(transaction):
        encoded_transaction_text = transaction_encode(transaction)
        encoded_transaction_bytes = text_to_bytes(encoded_transaction_text)

        Network().send_transaction(encoded_transaction_bytes)
        logging.info('transaction broadcasted')
    @staticmethod
    def send_transaction_to_gateways(transaction, gateway_list):
        encoded_transaction_text = transaction_encode(transaction)
        encoded_transaction_bytes = text_to_bytes(encoded_transaction_text)
        
        
        for gateway in gateway_list:
            Network().send_transaction_to_gateways(encoded_transaction_bytes, gateway)

    def _is_valid_address_format(self, address_candidate):
        return ADDRESS_PATTERN.match(address_candidate)

    def _is_valid_ipfs_doc_format(self, ipfs_doc_txt):
        try:
            return float(ipfs_doc_txt) > 0
        except ValueError:
            return False
    
    def _on_new_gateway_list(self, host, port):
        
        
        if host not in gateway_list:
            gateway_list.append(host)
    
        print( gateway_list)
        
        self._quit()
        
    def _quit(self, signal, frame):
        logging.info("Stopping...")
        self.shutdown_event.set()
        self.GatewayListener.close()
        


