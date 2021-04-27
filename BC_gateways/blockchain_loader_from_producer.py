#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import config
from producer_blockchain import BlockchainProducer
from block_producer import Block
from encoder_producer import blockchain_encode, blockchain_decode
import os.path
import logging
from threading import Lock

class ProducerBlockchainLoader:
    lock = Lock()

    def __init__(self, location = None):
        self.blockchain_store_producer = location or config.get('producer_blockchain_store')

    def _load(self):
        if os.path.isfile(self.blockchain_store_producer):
            blockchain = blockchain_decode(open(self.blockchain_store_producer).read())
            print('GATEWAY:Loaded {} blocks from {} '.format(len(blockchain.chain), self.blockchain_store_producer))
            return blockchain
        else:
            blockchain = BlockchainProducer()
            genesis_block = Block()
            genesis_block.id = config.get('genesis_block_id')
            genesis_block
            blockchain.add_block(genesis_block)
            print('GATEWAY:No blockchain found, initialised new chain with genesis block')
            return blockchain

    def _save(self, blockchain):
        open(self.blockchain_store_producer, 'w').write(blockchain_encode(blockchain))

    def process(self, op):
        ProducerBlockchainLoader.lock.acquire()
        try:
            blockchain = self._load()
            result = op(blockchain)
            self._save(blockchain)
            return result
        finally:
            ProducerBlockchainLoader.lock.release()
