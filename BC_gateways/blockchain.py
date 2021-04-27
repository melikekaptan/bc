#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from crypto import Crypto
from config import config
import logging

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction_root = None

        self.difficulty        = config.get('difficulty')
        self.block_size        = config.get('block_size')
        self.block_reward      = config.get('block_reward')
      


    def get_last_block_id(self):
        #logging.info('last block id : {}'.format(self.chain[-1].id))
        return self.chain[-1].id

    def remove_last_block(self):
        self.chain.pop()
 
    def add_block(self, new_block):
        if len(self.chain) == 0:
            if new_block.id == config.get('genesis_block_id'):
                self.chain.append(new_block)
                return
            else:
                raise ValueError('First block to be added must be the genesis block with id {}'.format(config.get('genesis_block_id')))

        if self.get_last_block_id() != new_block.previous_block_id:
            raise ValueError('Refused to add new block, previous_block_id {} does not match actual previous block {}'
                             .format(new_block.previous_block_id, self.get_last_block_id()))

        if not new_block.is_mined():
            raise ValueError('Refused to add new block, block has not been mined correctly')

        transaction_index = 0
        transaction_ids_for_new_block = set()

        print('GATEWAY: transaction root for new block : {}'.format(new_block.transaction_root))

      

        self.chain.append(new_block)

    def get_blocks_following(self, root_block_id):
        root_block_index = None
        print("get blocks following : " + root_block_id)
        print(type(root_block_id))
       
    
        try:
            for index, block in enumerate(self.chain):
                print(index, block, block.id)
                if str(block.id) == str(root_block_id):
                    root_block_index = index + 1                

        except StopIteration:
            return None

        return self.chain[root_block_index:]

    def has_transaction(self, transaction):
        return any(map(lambda b : b.has_transaction(transaction), self.chain))
    
    
    
    
