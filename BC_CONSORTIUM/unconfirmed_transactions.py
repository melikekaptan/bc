#!/usr/bin/env python3

import logging
from threading import Lock


class UnconfirmedTransactions:
    lock = Lock()
    
    def __init__(self):
        self.transactions = {}

    def add(self, transaction):
        self.transactions[transaction.id] = transaction

    def get(self):
        return self.transactions

    def get_transactions(self):
        return self.transactions.values()

    def remove(self, transaction):
        if transaction.id in self.transactions:
            del self.transactions[transaction.id]
            
    #def discard_transaction(self):

       #items = self.get_transactions()
       #rem = self.get()
       #logging.info('unconfirmed transaction  : {}'.format(self.transactions))
       
       #for transaction in self.transactions:
           #i = transaction.id
          # print("i:   " + i)
       #logging.info('unconfirmed transaction selected : {}'.format(rem))
       
      
          
    
