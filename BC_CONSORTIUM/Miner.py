#!/usr/bin/env python3

from threading import Thread
import logging
from hash import hash_string, hash_string_to_hex
from encoders import block_encode, transaction_encode, transaction_to_dict
from block import Block
from crypto import Crypto
from blockchain_loader import BlockchainLoader
from transaction_helper import build_transaction
from unconfirmed_transactions_loader import UnconfirmedPaymentsLoader
from unconfirmed_transactions import UnconfirmedTransactions
from transaction import Transaction
from multiprocessing import Queue
from threading import Lock
from config import config
import time

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
        logging.info('{} started'.format(SERVICE_NAME))
        

        while not self.shutdown_event.is_set():
 
            while not self.work_queue.empty():
               
                self.current_unmined_block = Block()
                self.current_unmined_block.previous_block_id = self._get_last_block_id_from_blockchain()
                _block_count = 0
              
                while _block_count != config.get('block_size'):
                    #logging.info('queue size : {} '.format(self.work_queue.qsize()))
                    work_item = self.work_queue.get()
                    print('CONSORTIUM: {} \n \
                    is taken from queue to be added to the block'.format(work_item.id))
                   
                   # transaction = self._build_mining_transaction(work_item)
                    #if not Crypto.validate_transaction(hash_string_to_hex(transaction_encode(work_item))):
                    if not Crypto.validate_transaction(work_item):
                        print('CONSORTIUM: {} received invalid transaction (invalid signature)'.format(SERVICE_NAME))
                        continue
        
                    if self.current_unmined_block.has_transaction(work_item):
                        print('CONSORTIUM: {} ignoring transaction, already added to current block'.format(SERVICE_NAME))
                        continue
        
                    if self._is_transaction_already_in_blockchain(work_item):
                        print('CONSORTIUM: {} ignoring transaction, already in blockchain'.format(SERVICE_NAME))
                        continue
                    
                    if self._is_transaction_with_same_document_already_in_blockchain(work_item):
                        print('CONSORTIUM: {} ignoring transaction, same document is already in blockchain'.format(SERVICE_NAME))
                        continue
                    
                    if work_item == STOP_WORKING:
                        break
                    
                    self.current_unmined_block.add(work_item)
                    _block_count += 1
                    print("added work_item to current_unmined_block, block count is : " .format(_block_count))   
    
                if self.current_unmined_block.is_mineable():
   
                    if len(self.current_unmined_block.transactions) != 0:
                        mined_block = self._mine(self.current_unmined_block)
                        if mined_block:
                            mined_block.id = hash_string_to_hex(block_encode(mined_block))
                            logging.info('{} mined new block! nonce={} id={}'.format(SERVICE_NAME, str(mined_block.nonce), mined_block.id))
                            self.on_new_block(mined_block)
                           
                        else:
                            logging.info('{} mining of current block abandoned'.format(SERVICE_NAME))

        logging.info('{} waiting for work...'.format(SERVICE_NAME))       
        logging.info('{} shut down'.format(SERVICE_NAME))

    def stop(self):
        self.work_queue.put(STOP_WORKING)

    def _get_transactions_unconfirmed(self):
        _queue = Queue()

        def discard_transaction(unconfirmed_transactions):
            #print(unconfirmed_transactions.transactions)
            gotransaction = unconfirmed_transactions.get_transactions()
            for transaction in gotransaction:
                logging.info('unconfirmed transaction1 :    {}'.format(str(transaction)))
                if transaction.from_address == 'ede07bbcea76f5ac1f7435f477db270582c99620a6d9a9379732e6f3a64272bb':
                
                    item = unconfirmed_transactions.transactions[transaction.id]
                    #logging.info('unconfirmed transaction signature :    {}'.format(item.signature))
                    _queue.put(item, block = True)
                    logging.info('{} unconfirmed transactions added to first queue : '.format(_queue.qsize()))
                 
            return _queue
        return UnconfirmedPaymentsLoader().process(discard_transaction)
    
    def _delete_transactions_unconfirmed(self, work_item):

        def delete_transaction(unconfirmed_transactions):
            logging.info('entered delete')
            logging.info('work_item : {}'.format(work_item))
            #print(unconfirmed_transactions.transactions)    
            try:
                #if work_item in unconfirmed_transactions.transactions:
                #logging.info('unconfirmed transaction2 :    {}'.format(str(work_item)))
                del unconfirmed_transactions.transactions[work_item.id]
                logging.info('work item id in transactions deleted : {}'.format(work_item.id))
            except:
                import pdb
                pdb.set_trace()
            #return unconfirmed_transactions
        return UnconfirmedPaymentsLoader().process(delete_transaction)

    #def form_queue(self):
     #   ut = self._get_transactions_unconfirmed()
      #  logging.info('{} unconfirmed transactions added to first queue : '.format(ut.qsize()))
       # _queue_ = Queue()
        #for i in range(ut.qsize()):
         #   transaction = ut.get()
          #  if _queue_.put(transaction, block = True) is not None:
           #     UnconfirmedPaymentsLoader().process(lambda u_t : u_t.remove(transaction))
        #logging.info('{} unconfirmed transactions added to second queue : '.format(_queue_.qsize()))    
        #return _queue_
        #logging.info('queue2 :    {}'.format(sig.signature))
        #return ut
        #logging.info('{} transaction dictionary is here'.format(transactions_selected))
        #for transaction in transactions_selected:
            #logging.info('{} transaction will be put into the queue with signature '.format(transaction))
            #transaction = transaction_to_dict(transactions_selected)
   

    def _get_last_block_id_from_blockchain(self):
        ret = BlockchainLoader().process(lambda x : x.get_last_block_id())
        #logging.info('block miner bringing last block id : {}'.format(ret))
        return ret

    def _is_transaction_already_in_blockchain(self, transaction):
        return BlockchainLoader().process(lambda blockchain : blockchain.has_transaction(transaction))
    
    def _is_transaction_with_same_document_already_in_blockchain(self, transaction):
        return BlockchainLoader().process(lambda blockchain : blockchain.has_transaction_with_same_document(transaction))

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
