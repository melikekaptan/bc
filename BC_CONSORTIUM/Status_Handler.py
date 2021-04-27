#!/usr/bin/env python3

from network import Network
from blockchain_loader import BlockchainLoader
from utils import text_to_bytes, bytes_to_text
from encoders import block_list_decode
import logging
import sys

class StatusHandler:
    def __init__(self, on_valid_block = lambda b: b):
        self.on_valid_block = on_valid_block

    def handle_status_update(self, blockchain_length, host, port):
        print('handle_status_update, press Ctrl-C to quit')
        def request_blocks_after(blockchain, block_id):
            new_blocks = self._get_new_blocks(host, port, block_id)
            print('CONSORTIUM: new_blocks arrived {}'.format(new_blocks))
            for new_block in new_blocks:
                blockchain.add_block(new_block)
                self.on_valid_block(new_block)
            print('CONSORTIUM: Received {} new blocks from {}:{}'.format(len(new_blocks), host, port))
        
            return len(new_blocks)

        def update_blockchain(blockchain):
            logging.debug('my chain lenght: {} ' .format(len(blockchain.chain)))
            if int(blockchain_length) > len(blockchain.chain):
                print('blockchain_length > len(blockchain.chain), press Ctrl-C to quit')
                while not request_blocks_after(blockchain, blockchain.get_last_block_id()):
                    blockchain.remove_last_block()

            else:
                print('CONSORTIUM: my chain lenght: {} bigger than the {} ' .format(len(blockchain.chain), host))
                print('CONSORTIUM: Host {}:{} has {} blocks, ignoring because we already have {}'.format(host, port,blockchain_length, len(blockchain.chain)))
               # blockchain.get_blocks_following(blockchain_length)
        BlockchainLoader().process(update_blockchain)

    def _get_new_blocks(self, host, port, last_block_id):
        #logging.info('last_block_id {}'.format(last_block_id))
        last_block_id_bytes = text_to_bytes(str(last_block_id))
        new_blocks_bytes = Network().send_block_request_and_wait(last_block_id_bytes, host, port)
        print('CONSORTIUM: new_blocks_bytes {} \n with lenght {}' .format(new_blocks_bytes, len(new_blocks_bytes)))
        if len(new_blocks_bytes):
            new_blocks_json = bytes_to_text(new_blocks_bytes)
            return block_list_decode(new_blocks_json)
        else:
            # Unknown block requested, so probably the chain has forked
            return []
