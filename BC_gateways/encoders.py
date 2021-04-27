#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 23:56:51 2019

@author: melike
"""

from blockchain import Blockchain
from block2 import Block
from transaction import Transaction
import logging
from root import RootMiner
from root import RootElement
import json

def blockchain_decode(blockchain_json):
    blockchain_dict = json.loads(str(blockchain_json))

    blockchain = Blockchain()
    for block_dict in blockchain_dict['chain']:
        #print(block_dict)
        block = block_from_dict(block_dict)
        blockchain.add_block(block)

    return blockchain
######################################################################################
def rootchain_decode(rootchain_json):
    rootchain_dict = json.loads(str(rootchain_json))

    root = RootMiner()
    for root_dict in rootchain_dict['root_chain']:
        print(root_dict)
        root_element = root_from_dict(root_dict)
        root.add_root(root_element)

    return root

def root_from_dict(root_dict):
    root_element = RootElement()
    root_element.transaction_root = root_dict['transaction_root']
    root_element.transactions = root_dict['transactions']
    
    return root_element

def rootchain_encode(root_records):
    rootchain_dict = rootchain_to_dict(root_records)
    return json.dumps(rootchain_dict, sort_keys=True)

def rootchain_to_dict(root_records):
    return {'root_chain' : list(map(root_to_dict, root_records.root_chain))}

def root_to_dict(RootElement):
   
    return {
        'transaction_root' : RootElement.transaction_root,
        'transactions' : list(map(transaction_in_root_to_dict, RootElement.transactions))
    }
    
def transaction_in_root_to_dict(transaction):
    return {
        'from_gateway' : transaction['from_gateway'],
        'ipfs_doc'     : transaction['ipfs_doc'],
        'model'        : transaction['model'],
        'timestamp'    : transaction['timestamp'],
        'public_key'   : transaction['public_key'],
        'signature'    : transaction['signature'],
        'id'           : transaction['id']
    }

    
####################################################################################3

def blockchain_to_dict(blockchain):
    return {'chain' : list(map(block_to_dict, blockchain.chain))}

def blockchain_encode(blockchain):
    blockchain_dict = blockchain_to_dict(blockchain)
    return json.dumps(blockchain_dict, sort_keys=True)

def block_from_dict(block_dict):
    block = Block()
    block.id = block_dict['id']
    block.previous_block_id = block_dict['previous_block_id']
    block.transaction_root = block_dict['transaction_root']
    block.proof = block_dict['nonce']
    return block

def block_to_dict(block):
    return {
        'id' : block.id,
        'previous_block_id' : block.previous_block_id,
        'transaction_root' :  block.transaction_root,
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
    block_list = json.loads(block_list_json)
    return list(map(block_from_dict, block_list))

def block_list_encode(block_list):
    return json.dumps(list(map(block_to_dict, block_list)))

def transaction_from_dict(transaction_dict):
    #logging.info('transaction_from_dict mapping transaction')
    transaction = Transaction(transaction_dict['from_gateway'], transaction_dict['ipfs_doc'],
        transaction_dict['model'], transaction_dict['public_key'])
    
    transaction.timestamp = transaction_dict['timestamp']
    transaction.signature = transaction_dict['signature']
    transaction.id        = transaction_dict['id']
    #logging.info('transaction_list_decode signature {}'.format(transaction.signature))
    #logging.info('transaction_list_decode id {}'.format(transaction.id))
    return transaction

def transaction_to_dict(transaction):
    return {
        'from_gateway' : transaction.from_gateway,
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