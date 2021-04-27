#!/usr/bin/env python3

import socket
from threading import Thread
from utils import bytes_to_text
import logging
import sys

SERVICE_NAME = 'Network Listener'
BUFFER_SIZE = 1024 * 1024
BACKLOG_SIZE = 5

class NetworkListener(Thread):
    def __init__(self, listener_port, shutdown_event, on_update):
        Thread.__init__(self)
        self.listener_port = listener_port
        self.shutdown_event = shutdown_event
        self.on_update = on_update

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', self.listener_port))
        print("socket bind")
        print('CONSORTIUM: {} listening for status updates on port {}...'.format(SERVICE_NAME, self.listener_port))
        
        while not self.shutdown_event.is_set():
            try:
                bytes, addr = self.socket.recvfrom(BUFFER_SIZE)
                status_value, Chain_Synchronization_port = bytes_to_text(bytes).split(':')
                host = addr[0]
                print('CONSORTIUM: {} new status update of {} from {}:{}'.format(SERVICE_NAME, status_value, host, Chain_Synchronization_port))
                self.on_update(int(status_value), host, int(Chain_Synchronization_port))

            except OSError:
                print('CONSORTIUM: {} error; {}'.format(SERVICE_NAME, sys.exc_info()))
                pass # probably close() was called

            except Exception:
                logging.error('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))

        print('CONSORTIUM: {} shut down'.format(SERVICE_NAME))

    def close(self):
        self.socket.close()
