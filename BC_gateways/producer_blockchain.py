#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from crypto import Crypto
from config import config
import logging

class BlockchainProducer:
    def __init__(self):
        self.chain = []
        self.transactions = []

        self.difficulty        = config.get('difficulty')
        self.block_size        = config.get('block_size')
        self.block_reward      = config.get('block_reward')
      


    def get_last_block_id(self):
        #logging.info('last block id : {}'.format(self.chain[-1].id))
        return self.chain[-1].id

    def remove_last_block(self):
        self.chain.pop()
       # last_block = self.blocks.pop()
        #for transaction in last_block.transactions:
         #   from_address = transaction.from_address
          #  ipfs_doc   = transaction.ipfs_doc
           # model       = transaction.model
            
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

        transaction_index = 0
        transaction_ids_for_new_block = set()

        for transaction in new_block.transactions:
            if not Crypto.validate_transaction(transaction):
                raise ValueError('Invalid transaction in new block (bad signature): {}'.format(transaction))

            if self.has_transaction(transaction):
                raise ValueError('Transaction with id {} already exists within the blockchain'.format(transaction.id))

            if transaction.id in transaction_ids_for_new_block:
                raise ValueError('Duplicate transaction in new block, id: {}'.format(transaction.id))

            transaction_ids_for_new_block.add(transaction.id)
            #logging.info(' transaction ids for new block : {}'.format(transaction_ids_for_new_block))


            from_address = transaction.from_address
            ipfs_doc   = transaction.ipfs_doc
            model       = transaction.model
            
            if transaction_index != len(new_block.transactions) - 1:

                transaction_index += 1

        self.chain.append(new_block)
        #logging.info('chain for new block : {}'.format(self.chain))
        #self.address_balances = address_balances

    def get_blocks_following(self, root_block_id):
        root_block_index = None
        print("get blocks following : " + root_block_id)
        print(type(root_block_id))
        print(type(self.chain))
        #if not root_block_id:
         #   root_block_index = 0
       
    
        try:
            for index, block in enumerate(self.chain):
                print(index, block, block.id)
                if str(block.id) == str(root_block_id):
                    print('yes')
                    #print("root_block_id = " + index)
                    print('yes')
                    root_block_index = index + 1                

        except StopIteration:
            return None

        return self.chain[root_block_index:]

    def has_transaction(self, transaction):
        return any(map(lambda b : b.has_transaction(transaction), self.chain))
