#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from threading import Thread
import logging
import sys
from utils import bytes_to_text
from encoders import transaction_decode

SERVICE_NAME = 'Transaction StatusHandler'
BUFFER_SIZE = 1024 * 1024
BACKLOG_SIZE = 3

class TransactionStatusHandler(Thread):
    def __init__(self, listener_port, shutdown_event, on_new_transaction):
        Thread.__init__(self)
        self.listener_port = listener_port
        self.shutdown_event = shutdown_event
        self.on_new_transaction = on_new_transaction

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', self.listener_port))
        logging.info('{} listening for new transactions on port {}...'.format(SERVICE_NAME, self.listener_port))

        while not self.shutdown_event.is_set():
            try:
                bytes, addr = self.socket.recvfrom(BUFFER_SIZE)
                transaction_text = bytes_to_text(bytes)
                transaction = transaction_decode(transaction_text)

                logging.info('{} received new transaction for amount {} from {}'.format(SERVICE_NAME, transaction.ipfs_doc, addr[0]))
                self.on_new_transaction(transaction)
                logging.info('{} added new transaction {} '.format(SERVICE_NAME, self.on_new_transaction))
                

            except OSError:
                logging.debug('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))
                pass

            except Exception:
                logging.error('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))

        logging.info('{} shut down'.format(SERVICE_NAME))

    def close(self):
        self.socket.close()
