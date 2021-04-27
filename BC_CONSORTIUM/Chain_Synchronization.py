#!/usr/bin/env python3

import socket
from threading import Thread
import sys
import logging
from encoders import block_encode, block_list_encode
from utils import bytes_to_text, text_to_bytes
from blockchain_loader import BlockchainLoader

SERVICE_NAME = 'Chain Synchronization Server'
BUFFER_SIZE = 1024 * 1024
BACKLOG_SIZE = 3

class ChainSynchronization(Thread):
    def __init__(self, listener_port, shutdown_event):
        Thread.__init__(self)
        self.listener_port = listener_port
        self.shutdown_event = shutdown_event
        self.socket = None

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', self.listener_port))
        self.socket.listen(BACKLOG_SIZE)
        print('CONSORTIUM: {} started, listening on port {}...'.format(SERVICE_NAME, self.listener_port))

        connection = None
        while not self.shutdown_event.is_set():
            try:
                connection, addr = self.socket.accept()
                logging.info('{} received new request from {}'.format(SERVICE_NAME, addr[0]))
                request_bytes = connection.recv(BUFFER_SIZE)
                self._on_block_request(connection, request_bytes)

            except ConnectionAbortedError:
                logging.debug('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))
                pass

            except Exception:
                logging.error('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))
                if connection:
                    connection.close()

        print('CONSORTIUM: {} shut down'.format(SERVICE_NAME))

    def close(self):
        self.socket.close()

    def _on_block_request(self, connection, request_bytes):
        block_id = bytes_to_text(request_bytes)
        logging.info('{} request for blocks following {}'.format(SERVICE_NAME, block_id))

        new_blocks = BlockchainLoader().process(lambda blockchain : blockchain.get_blocks_following(block_id))

        if new_blocks is not None:
            new_blocks_json = block_list_encode(new_blocks)
            new_blocks_bytes = text_to_bytes(new_blocks_json)
            leng = text_to_bytes(str(len(new_blocks_bytes)))
            connection.send(leng)
            res = connection.recv(BUFFER_SIZE)
            if bytes_to_text(res) == 'OK':
                connection.sendall(new_blocks_bytes)
                logging.info('{} sent {} new blocks {} bytes'.format(SERVICE_NAME, len(new_blocks), len(new_blocks_bytes)))
        else:
            logging.info('{} unknown block requested: {}'.format(SERVICE_NAME, block_id))
            
        connection.close()
