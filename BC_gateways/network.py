#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import logging
from config import config
from network_listener import NetworkListener
from contextlib import closing
from utils import bytes_to_text, text_to_bytes

BROADCAST_ADDRESS = '255.255.255.255'
BUFFER_SIZE = 1024 * 1024

service_name = 'NETWORK'
class Network:
    def __init__(self):
        pass

    def send_transaction(self, bytes):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(bytes, (BROADCAST_ADDRESS, config.get('transaction_port')))

    def send_block_request_and_wait(self, bytes, host, port):
        logging.info('requesting new blocks from {}'.format(host))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print("NETWORK connected")
        s.send(bytes)
        
        block_len = s.recv(1024)
        chunk = b""
        if int(block_len) > 0:
            s.send(text_to_bytes('OK'))
            block_data_len = 0
            while block_data_len < int(block_len):
                block_data = s.recv(BUFFER_SIZE)
                block_data_len = block_data_len + len(block_data)
                #print("received:")
                #print('GATEWAY:{} received new block data from {}:{}  string length is ; {}'.format(service_name, host, port, len(block_data)))
                chunk += block_data

                
            s.close()
    
            print('GATEWAY: received new block data from {}:{} {}'.format(host, port, chunk))
     
        return chunk

    def find_host_to_sync(self, on_host_found, shutdown_event):
        print('finding host to sync')
        Network_Listener_port = config.get('Network_Broadcast_Port')
        logging.info('found host to syncronize')
        listener = NetworkListener(Network_Listener_port, shutdown_event, on_host_found)
        listener.start()
        return listener
