#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 23:56:51 2019

@author: melike
"""

from producer_blockchain import BlockchainProducer
from block_producer import Block
from transaction_producer import TransactionProducer
import logging
import sys
import json

def blockchain_decode(blockchain_json):
    
    blockchain_dict = json.loads(blockchain_json, object_pairs_hook=dict, object_hook=list)
    blockchain = BlockchainProducer()
    if blockchain_dict['chain']:
        for block_dict in blockchain_dict['chain']:
            block = block_from_dict(block_dict)
            blockchain.add_block(block)

    return blockchain

def blockchain_to_dict(blockchain):
    return {'chain' : list(map(block_to_dict, blockchain.chain))}

def blockchain_encode(blockchain):
    blockchain_dict = blockchain_to_dict(blockchain)
    return json.dumps(blockchain_dict, sort_keys=True)

def block_from_dict(block_dict):
    block = Block()
    block.id = block_dict['id']
    block.previous_block_id = block_dict['previous_block_id']
    block.transactions = list(map(transaction_from_dict, block_dict['transactions']))
    block.proof = block_dict['nonce']
    return block

def block_to_dict(block):
    return {
        'id' : block.id,
        'previous_block_id' : block.previous_block_id,
        'transactions' : list(map(transaction_to_dict, block.transactions)),
        'nonce' : block.proof
    }

def block_decode(block_json):
    block_dict = json.loads(block_json)
    return block_from_dict(block_dict)

def block_encode(block, include_id = False):
    block_dict = block_to_dict(block)
    if not include_id:
        block_dict['id'] = None
    return json.dumps(block_dict, sort_keys=True)

def block_list_decode(block_list_json):
    try:
        block_list = json.loads(block_list_json)
        #block_list = [json.loads(line) for line in block_list_json]
    except Exception:
        logging.error('{} error: {}'.format('Encoders', sys.exc_info()))
    return list(map(block_from_dict, block_list))

def block_list_encode(block_list):
    return json.dumps(list(map(block_to_dict, block_list)))

def transaction_from_dict(transaction_dict):
    #logging.info('transaction_from_dict mapping transaction')
    transaction = TransactionProducer(transaction_dict['from_address'], transaction_dict['ipfs_doc'],
        transaction_dict['model'], transaction_dict['public_key'])
    
    transaction.timestamp = transaction_dict['timestamp']
    transaction.signature = transaction_dict['signature']
    transaction.id        = transaction_dict['id']
    #logging.info('transaction_list_decode signature {}'.format(transaction.signature))
    #logging.info('transaction_list_decode id {}'.format(transaction.id))
    return transaction

def transaction_to_dict(transaction):
    return {
        'from_address' : transaction.from_address,
        'ipfs_doc'     : transaction.ipfs_doc,
        'model'        : transaction.model,
        'timestamp'    : transaction.timestamp,
        'public_key'   : transaction.public_key,
        'signature'    : transaction.signature,
        'id'           : transaction.id
    }

def transaction_decode(transaction_json):
    transaction_dict = json.loads(transaction_json)
    return transaction_from_dict(transaction_dict)

def transaction_encode(transaction):
    return json.dumps(transaction_to_dict(transaction), sort_keys=True)

def transaction_list_decode(read_transaction_list):
    #logging.info('transaction_list_decode take the file')
    #read_transaction_list = open(transaction_list_json, "w+").read()
    #logging.info('transaction_list_decode open the file')
    transaction_list = json.loads(str(read_transaction_list))
    #logging.info('transaction_list_decode load the file')
    return list(map(transaction_from_dict, transaction_list))

def transaction_list_encode(transaction_list):
    return json.dumps(list(map(transaction_to_dict, transaction_list)))