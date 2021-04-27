#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from network import Network
from blockchain_loader_from_producer import ProducerBlockchainLoader
from utils import text_to_bytes, bytes_to_text
from encoder_producer import block_list_decode
import logging
import sys

class ProducerStatusHandler:
    def __init__(self):
        pass

    def handle_status_update(self, blockchain_length, host, port):
        print('handle_status_update, press Ctrl-C to quit')
        def request_blocks_after(blockchain, block_id):
            new_blocks = self._get_new_blocks(host, port, block_id)
            #logging.info('new_blocks arrived {}'.format(new_blocks))
            for new_block in new_blocks:
                blockchain.add_block(new_block)
                #self.on_valid_block(new_block)
            print('GATEWAY:Received {} new blocks from {}:{}'.format(len(new_blocks), host, port))
        
            return len(new_blocks)

        def update_blockchain(blockchain):
            #logging.info('my chain lenght: {} ' .format(len(blockchain.chain)))
            if int(blockchain_length) > len(blockchain.chain):
                print('blockchain_length > len(blockchain.chain), press Ctrl-C to quit')
                while not request_blocks_after(blockchain, blockchain.get_last_block_id()):
                    blockchain.remove_last_block()

            #else:
                #logging.info('my chain lenght: {} bigger than the {} ' .format(len(blockchain.chain), host))
                #logging.info('Host {}:{} has {} blocks, ignoring because we already have {}'.format(host, port,blockchain_length, len(blockchain.chain)))
               # blockchain.get_blocks_following(blockchain_length)
        ProducerBlockchainLoader().process(update_blockchain)

    def _get_new_blocks(self, host, port, last_block_id):
        #logging.info('last_block_id {}'.format(last_block_id))
        last_block_id_bytes = text_to_bytes(str(last_block_id))
        new_blocks_bytes = Network().send_block_request_and_wait(last_block_id_bytes, host, port)
        logging.info('new_blocks_bytes with lenght {}' .format(len(new_blocks_bytes)))
        if len(new_blocks_bytes):
            new_blocks_json = bytes_to_text(new_blocks_bytes)
            return block_list_decode(new_blocks_json)
        else:
            return []
