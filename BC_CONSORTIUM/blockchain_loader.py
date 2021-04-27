#!/usr/bin/env python3

from config import config
from blockchain import Blockchain
from block import Block
from encoders import blockchain_encode, blockchain_decode
import os.path
import logging
from threading import Lock

class BlockchainLoader:
    lock = Lock()

    def __init__(self, location = None):
        self.blockchain_store = location or config.get('blockchain_store')

    def _load(self):
        #print(os.stat(self.blockchain_store).st_size)
        
        #print(os.stat(self.blockchain_store).st_size)
        if os.path.isfile(self.blockchain_store) and os.stat(self.blockchain_store).st_size != 0:
            blockchain = blockchain_decode(open(self.blockchain_store).read())
            #print('CONSORTIUM: Loaded {} blocks from {} '.format(len(blockchain.chain), self.blockchain_store))
            
            return blockchain
        
        else:
            blockchain = Blockchain()
            genesis_block = Block()
            genesis_block.id = config.get('genesis_block_id')
            genesis_block
            blockchain.add_block(genesis_block)
            print('CONSORTIUM: No blockchain found, initialised new chain with genesis block')
            return blockchain

    def _save(self, blockchain):
        open(self.blockchain_store, 'w').write(blockchain_encode(blockchain))

    def process(self, op):
        BlockchainLoader.lock.acquire()
        try:
            blockchain = self._load()
            result = op(blockchain)
            self._save(blockchain)
            return result
        finally:
            BlockchainLoader.lock.release()
