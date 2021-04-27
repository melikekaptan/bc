#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        if os.path.isfile(self.blockchain_store):
            blockchain = blockchain_decode(open(self.blockchain_store).read())
            #logging.info('Loaded {} blocks from {} '.format(len(blockchain.chain), self.blockchain_store))
            return blockchain
        else:
            blockchain = Blockchain()
            genesis_block = Block()
            genesis_block.id = config.get('genesis_block_id')
            genesis_block
            blockchain.add_block(genesis_block)
            logging.info('No blockchain found, initialised new chain with genesis block')
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
