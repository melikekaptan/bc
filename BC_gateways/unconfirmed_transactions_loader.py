#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import config
from unconfirmed_transactions import UnconfirmedTransactions
from encoders import transaction_list_encode, transaction_list_decode, transaction_decode
import os.path
import logging
from threading import Lock

class UnconfirmedPaymentsLoader:
    lock = Lock()

    def __init__(self):
        self.transactions_store = 'blockchain_pending.json'
    def _load(self):
        unconfirmed_transactions = UnconfirmedTransactions()
        logging.info('true')
        if os.path.isfile(self.transactions_store):
            logging.info('true')
            read_transaction_list = open(self.transactions_store).read()
            unconfirmed_transactions_list = transaction_list_decode(read_transaction_list)
            logging.debug('Loaded {} unconfirmed transaction from {}'.format(len(unconfirmed_transactions_list), self.transactions_store))
            for unconfirmed_transaction in unconfirmed_transactions_list:
                unconfirmed_transactions.add(unconfirmed_transaction)
                iden = unconfirmed_transaction.signature
        else:
            logging.info('false')

        return unconfirmed_transactions

    def _save(self, unconfirmed_transactions):
        transaction_list = unconfirmed_transactions.transactions.values()
        logging.info('transaction list values saved : {}'.format(transaction_list))
        open(self.transactions_store, 'w').write(transaction_list_encode(transaction_list))

    def process(self, op):
        UnconfirmedPaymentsLoader.lock.acquire()
        try:
            unconfirmed_transactions = self._load()
            result = op(unconfirmed_transactions)
            self._save(unconfirmed_transactions)
            return result
        finally:
            UnconfirmedPaymentsLoader.lock.release()
            
  
        
            
