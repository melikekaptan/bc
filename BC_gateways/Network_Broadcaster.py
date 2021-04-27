#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
import socket
from utils import text_to_bytes
from blockchain_loader import BlockchainLoader
import logging

SERVICE_NAME = 'Network Broadcaster'
BROADCAST_ADDRESS = '255.255.255.255'

class NetworkBroadcaster(Thread):
    def __init__(self, broadcast_port, Chain_Synchronization_port, broadcast_interval_seconds, shutdown_event):
        Thread.__init__(self)
        self.broadcast_port = broadcast_port
        self.Chain_Synchronization_port = Chain_Synchronization_port
        self.broadcast_interval_seconds = broadcast_interval_seconds
        self.shutdown_event = shutdown_event

    def run(self):
        while not self.shutdown_event.is_set():
            self._broadcast_status()
            self.shutdown_event.wait(self.broadcast_interval_seconds)
        logging.info('{} shut down'.format(SERVICE_NAME))

    def _broadcast_status(self):
        blockchain_length = self._get_blockchain_status_value()
        status_message_bytes = text_to_bytes('{}:{}'.format(blockchain_length, self.Chain_Synchronization_port))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(status_message_bytes, (BROADCAST_ADDRESS, self.broadcast_port))
        s.close()

    def _get_blockchain_status_value(self):
        return BlockchainLoader().process(lambda blockchain : len(blockchain.chain))
