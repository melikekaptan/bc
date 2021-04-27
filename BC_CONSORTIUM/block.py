#!/usr/bin/env python3

from config import config
from hash import hash_string
import encoders
import math
import hashlib
import logging
import json
from transaction import Transaction

class Block:
    def __init__(self):
        self.id = None
        self.timestamp = None
        self.proof = None
        self.previous_hash = None
        self.transactions = []
        self.previous_block_id = None
        

    def add(self, transaction):
        self.transactions.append(transaction)

    def has_transaction(self, transaction):
        return next((True for t in self.transactions if t.id == transaction.id), False)
    
    def has_transaction_with_same_document(self, transaction):
        return next((True for t in self.transactions if t.ipfs_doc == transaction.ipfs_doc), False)

    def set_nonce(self, proof):
        self.proof = proof

    def is_mineable(self):
        #if self.previous_block_id == config.get('genesis_block_id'):
         #   return True
        #if (len(self.transactions) >= config.get('block_size')  - 1):  #mining reward transaction will be added
        return True
 
   # def hash(self):
    #    encoded_block = json.dumps(self, sort_keys = True).encode()
     #   return hashlib.sha256(encoded_block).hexdigest()
    

    def is_mined(self):
        #block_hash_bytes = hash_string(encoders.block_encode(self, False))
        block_hash_bytes = hashlib.sha256((encoders.block_encode(self, False)).encode())
        hexa = block_hash_bytes.hexdigest()
        logging.info('hash of the unmined block:{}  '.format(hexa))
        y = bytes.fromhex(hexa)
        logging.info('binary version of hash:{} '.format(y))
        leading_zero_bits = self._count_leading_zero_bits_in_bytes(y)
        return leading_zero_bits >= config.get('difficulty')

    def _count_leading_zero_bits_in_bytes(self, bytes):
        count = 0

        for b in bytes:
            leading_zero_bits_in_byte = self._count_leading_zero_bits_in_byte(b)
            count += leading_zero_bits_in_byte
            if leading_zero_bits_in_byte < 8:
                return count

        return count

    def _count_leading_zero_bits_in_byte(self, b):
        return 8 - math.floor(math.log(b, 2)) - 1 if b else 8