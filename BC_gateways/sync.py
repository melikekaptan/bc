#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from network import Network
from Status_Handler import StatusHandler
from blockchain_loader import BlockchainLoader
from unconfirmed_transactions_loader import UnconfirmedPaymentsLoader
from send import SendCommand
from config import config
import signal
import logging
from threading import Event, Timer

class SyncCommand:

    def __init__(self, *args):
        if len(args) != 0:
            logging.error('wrong number of args for {}'.format(SyncCommand))

        else:
            self.shutdown_event = Event()
            self.broadcast_interval = config.get('transaction_broadcast_interval_seconds')
            on_status_update = StatusHandler().handle_status_update()
            print("on status update:" )
            logging.info('on status update return {}'.format(on_status_update))
            Network().find_host_to_sync(on_status_update, self.shutdown_event)

            signal.signal(signal.SIGINT, self._quit)

            print('Synchronising with the network, press Ctrl-C to quit')
            self._sync_unconfirmed_payments()
            self._send_unconfirmed_payments()

    def _sync_unconfirmed_payments(self):
        def read_unconfirmed_payments(unconfirmed_transactions):
            transactions = unconfirmed_transactions.get_transactions()
            print("got transactions")
            logging.info('got transactions {}'.format(transactions))

            def read_blockchain_and_sync(blockchain):
                transactions_to_remove = [t for t in transactions if blockchain.has_transaction(t)]
                for transaction in transactions_to_remove:
                    unconfirmed_transactions.remove(transaction)

            if len(transactions):
                BlockchainLoader().process(read_blockchain_and_sync)

        UnconfirmedPaymentsLoader().process(read_unconfirmed_payments)

    def _send_unconfirmed_payments(self):
        def send(unconfirmed_payments):
            print("i am sending unconfirmed payments")
            for transaction in unconfirmed_payments.get_transactions():
                print(transaction)
                SendCommand.send_transaction(transaction)

        UnconfirmedPaymentsLoader().process(send)
        self.broadcast_timer = Timer(self.broadcast_interval, self._send_unconfirmed_payments)
        #while not self._quit:
        self.broadcast_timer.start()
        print('timer started')
      
        
    def _on_new_block(self, new_block):
        for transaction in new_block.transactions:
            UnconfirmedPaymentsLoader().process(lambda u_t : u_t.remove(transaction))

    def _quit(self, signal, frame):
        self.shutdown_event.set()
        self.listener.close()
        self.broadcast_timer.cancel()
