#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
import logging
from hash import hash_string, hash_string_to_hex, hash_to_hex
from encoders import block_encode, transaction_encode, transaction_to_dict
from block import Block
from crypto import Crypto
from blockchain_loader import BlockchainLoader
from transaction_helper import build_transaction
from unconfirmed_transactions_loader import UnconfirmedPaymentsLoader
from unconfirmed_transactions import UnconfirmedTransactions
from mined_root_loader import MinedRootLoader
from root import RootElement
from transaction import Transaction
from queue import Queue
from threading import Lock
import merkletools
from config import config

SERVICE_NAME = 'Miner'
STOP_WORKING = None

class Miner(Thread):

    def __init__(self, key, work_queue, difficulty, shutdown_event,
                 stop_mining_event, on_new_block):
        Thread.__init__(self)
        self.key = key
        self.work_queue = work_queue
        self.required_leading_zero_bits = difficulty
        self.shutdown_event = shutdown_event
        self.stop_mining_event = stop_mining_event
        self.on_new_block = on_new_block
        self.current_unmined_block = Block()

    def run(self):
        #logging.info('{} started'.format(SERVICE_NAME))
        

        while not self.shutdown_event.is_set():
            while not self.work_queue.empty():
                self.current_unmined_block = Block()
                self.current_unmined_block.previous_block_id = self._get_last_block_id_from_blockchain() 
                print('GATEWAY: formed queue queue size:{} '.format(self.work_queue.qsize()))
                
                mt = merkletools.MerkleTools()  # default is sha256 
                _block_count = 0
                dictionary_for_root = RootElement()
                while _block_count != config.get('block_size'):
                    
                    list_for_dictionary = list()
                    print('GATEWAY:block count is: ' + format(_block_count))
                    work_item = self.work_queue.get()
                    print ('{} is taken from queue to be added to the block'.format(work_item.id))

                    if not Crypto.validate_transaction(work_item):
                        print('{} received invalid transaction (invalid signature)'.format(SERVICE_NAME))
                        continue
        
                    if self.current_unmined_block.has_transaction(work_item):
                        print('{} ignoring transaction, already added to current block'.format(SERVICE_NAME))
                        continue
        
                    if self._is_transaction_already_in_blockchain(work_item):
                        print('{} ignoring transaction, already in blockchain'.format(SERVICE_NAME))
                        continue
                    
                    if self._is_transaction_with_same_document_and_same_device_already_in_blockchain(work_item):
                        print('{} ignoring transaction, same update for same device already in blockchain'.format(SERVICE_NAME))
                        continue
                    
                    if dictionary_for_root.has_transaction_with_same_update_for_same_device(work_item):
                        print('{} ignoring transaction, already added to current block with same update for same device'.format(SERVICE_NAME))
                        continue
                    
                    if work_item == STOP_WORKING:
                        break
                    
                    w_i = transaction_to_dict(work_item) 
                    hex_data = hash_to_hex(str(transaction_to_dict(work_item)).encode('utf-8'))
                    
                    mt.add_leaf(hex_data)
                    dictionary_for_root.transactions.append(w_i)

                    print("added work_item to current_unmined_block")
                    #try:
                    #self._delete_transactions_unconfirmed(work_item)
                    #except:
                     #   import pdb
                     #   pdb.set_trace()
                    #continue
                    _block_count += 1
                    
                    if _block_count == config.get('block_size'):
                #Generates the merkle tree using the leaves that have been added.
                        leaf_count =  mt.get_leaf_count();
                        print(leaf_count)
                        mt.make_tree();
                        root_value = mt.get_merkle_root();  
                        dictionary_for_root.transaction_root = root_value
                        self.current_unmined_block.add(root_value) 
                
                if self.current_unmined_block.is_mineable():

                    logging.info('{}: unmined block is mineble'.format(SERVICE_NAME))
                    logging.info('{} started mining new block'.format(SERVICE_NAME))
                    
                    if root_value:
                        mined_block = self._mine(self.current_unmined_block)
                        if mined_block:
                            mined_block.id = hash_string_to_hex(block_encode(mined_block))
                            print('GATEWAY:{} mined new block! nonce={} id={}'.format(SERVICE_NAME, str(mined_block.nonce), mined_block.id))
                            self.on_new_block(mined_block)
                            self.record_tree(dictionary_for_root)
                           
                        else:
                            logging.info('{} mining of current block abandoned'.format(SERVICE_NAME))

        logging.info('{} waiting for work...'.format(SERVICE_NAME))       
        logging.info('{} shut down'.format(SERVICE_NAME))

    def stop(self):
        self.work_queue.put(STOP_WORKING)
        
        
    
    def record_tree(self,dictionary_for_root) :
        def add_newly_mined_root(root_records):
            root_records.add_root(dictionary_for_root)
            
        return MinedRootLoader().process(add_newly_mined_root)

   

    def _get_last_block_id_from_blockchain(self):
        ret = BlockchainLoader().process(lambda x : x.get_last_block_id())
        logging.info('block miner bringing last block id : {}'.format(ret))
        return ret

    def _is_transaction_already_in_blockchain(self, transaction):
        return BlockchainLoader().process(lambda blockchain : blockchain.has_transaction(transaction))
    
    def _is_transaction_with_same_document_and_same_device_already_in_blockchain(self, transaction):
        return MinedRootLoader().process(lambda root_records : root_records.has_transaction_with_same_update_for_same_device(transaction))
        
    def _is_transaction_with_same_update_for_same_device_already_in_current_unmined_block(self, work_item, transactions):
        if transactions is not []:
            for transaction in transactions:
                transaction_to_dict(transaction)
    
    def _mine(self, block):
        self.stop_mining_event.clear()

        nonce = 0
        while not self.shutdown_event.is_set() and not self.stop_mining_event.is_set():
            block.nonce = nonce

            if block.is_mined():
                return block
            #print(block.is_mined())
            nonce += 1
            block.proof = nonce
            logging.info('I am trying with nonce {}'.format(nonce))
