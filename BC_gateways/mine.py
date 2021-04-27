#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Event
from queue import Queue
import logging
import signal, sys

from config import config
from Chain_Synchronization import ChainSynchronization
from Network_Broadcaster import NetworkBroadcaster
from network_listener import NetworkListener
from listen_producer_block_chain import GatewayListener
from Status_Handler import StatusHandler
from Producer_Status_Handler import ProducerStatusHandler
from crypto import Crypto
from Transaction_Handler import TransactionStatusHandler
from Miner import Miner
from blockchain_loader import BlockchainLoader
from config import update_config_from_args


KEY_NAME = 'GW1234'

class MiningServer:
    def __init__(self):
        self.shutdown_event = Event()
        self.stop_mining_event = Event()

        Chain_Synchronization_port = config.get('Chain_Synchronization_port')
        self.Chain_Synchronization = ChainSynchronization(Chain_Synchronization_port, self.shutdown_event)

        Network_Broadcast_Port = config.get('Network_Broadcast_Port')
        network_broadcast_interval_seconds = config.get('network_broadcast_interval_seconds')
        self.Network_Broadcaster = NetworkBroadcaster(Network_Broadcast_Port, Chain_Synchronization_port,
                                                    network_broadcast_interval_seconds, self.shutdown_event)

        self.Status_Handler = StatusHandler(self._on_new_block_downloaded)
        self.Producer_Status_Handler = ProducerStatusHandler()
        Network_Listener_port = config.get('Network_Broadcast_Port')
        self.Network_Listener = NetworkListener(Network_Listener_port, self.shutdown_event, self._on_new_status)
        self.gateway_listener = GatewayListener(2606, self.shutdown_event, self._on_new_status_from_producers)
        crypto = Crypto()
        key = crypto.get_key(KEY_NAME) or crypto.generate_key(KEY_NAME)
        self.work_queue = Queue()
        difficulty = config.get('difficulty')
        self.Miner = Miner(key, self.work_queue, difficulty,
                                      self.shutdown_event, self.stop_mining_event, self._on_new_block_mined)
       

        Transaction_StatusHandler_port = config.get('transaction_port')
        self.Transaction_StatusHandler = TransactionStatusHandler(Transaction_StatusHandler_port, self.shutdown_event, self._on_new_transaction)

    def _quit(self, signal, frame):
        logging.info("Stopping...")
        self.shutdown_event.set()
        self.Chain_Synchronization.close()
        self.Network_Listener.close()
        self.Transaction_StatusHandler.close()
        self.gateway_listener.close()
        self.Miner.stop()

    def start(self):
        signal.signal(signal.SIGINT, self._quit)

        # Miners do several jobs...
        self.Network_Broadcaster.start()   # tell everyone else the length of the blockchain that we have
        self.Chain_Synchronization.start()         # listen for requests for the latest blockchain (from wallets or other miners)
        self.Network_Listener.start()      # listen for other miners telling us the length of their blockchains
        self.Transaction_StatusHandler.start() # listen for new transactions from wallets
        self.gateway_listener.start()
        self.Miner.start()          # mine new blocks

        self.shutdown_event.wait()
        logging.info("Main thread stopped")

    def _on_new_block_mined(self, block):
        BlockchainLoader().process(lambda blockchain : blockchain.add_block(block))

    def _on_new_block_downloaded(self, block):
        # we got a new block from elsewhere, stop mining current block someone else beat us to it
        self.stop_mining_event.set()

    def _on_new_transaction(self, transaction):
        self.work_queue.put(transaction)
        logging.info('put a new transaction to queue')

    def _on_new_status(self, blockchain_length, host, port):
        self.Status_Handler.handle_status_update(blockchain_length, host, port)
        
    def _on_new_status_from_producers(self, blockchain_length, host, port):
        self.Producer_Status_Handler.handle_status_update(blockchain_length, host, port)
    


if __name__ == '__main__':
    args = update_config_from_args(sys.argv)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

MiningServer().start()
