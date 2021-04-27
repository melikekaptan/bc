#!/usr/bin/env python3

from threading import Event
from multiprocessing import Queue
import logging
import signal, sys

from config import config
from Chain_Synchronization import ChainSynchronization
from Network_Broadcaster import NetworkBroadcaster
from Network_Listener import NetworkListener
from Status_Handler import StatusHandler
from crypto import Crypto
from Transaction_Handler import TransactionHandler
from Miner import Miner
from blockchain_loader import BlockchainLoader
from config import update_config_from_args

KEY_NAME = 'kaptan'

class MiningServer:
    def __init__(self):
        self.shutdown_event = Event()
        self.stop_mining_event = Event()

        Chain_Synchronization_port = config.get('Chain_Synchronization_port')
        self.Chain_Synchronization = ChainSynchronization(Chain_Synchronization_port, self.shutdown_event)

        Network_Broadcast_port = config.get('Network_Broadcast_port')
        Network_Broadcast_interval_seconds = config.get('Network_Broadcast_interval_seconds')
        self.Network_Broadcaster = NetworkBroadcaster(Network_Broadcast_port, Chain_Synchronization_port,
                                                    Network_Broadcast_interval_seconds, self.shutdown_event)

        self.Status_Handler = StatusHandler(self._on_new_block_downloaded)

        Network_Listener_port = config.get('Network_Broadcast_port')
        self.Network_Listener = NetworkListener(Network_Listener_port, self.shutdown_event, self._on_new_status)

        crypto = Crypto()
        key = crypto.get_key(KEY_NAME) or crypto.generate_key(KEY_NAME)
        self.work_queue = Queue()
        difficulty = config.get('difficulty')
        self.Miner = Miner(key, self.work_queue, difficulty,
                                      self.shutdown_event, self.stop_mining_event, self._on_new_block_mined)

        Transaction_Handler_port = config.get('transaction_port')
        self.Transaction_Handler = TransactionHandler(Transaction_Handler_port, self.shutdown_event, self._on_new_transaction)

    def _quit(self, signal, frame):
        logging.info("Stopping...")
        self.shutdown_event.set()
        self.Chain_Synchronization.close()
        self.Network_Listener.close()
        self.Transaction_Handler.close()
        self.Miner.stop()

    def start(self):
        signal.signal(signal.SIGINT, self._quit)
.
        self.Network_Broadcaster.start()   # tell everyone else the length of the blockchain that we have
        self.Chain_Synchronization.start()         # listen for requests for the latest blockchain (from wallets or other miners)
        self.Network_Listener.start()      # listen for other miners telling us the length of their blockchains
        self.Transaction_Handler.start() # listen for new transactions from wallets
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
        print('CONSORTIUM: put a new transaction to queue')

    def _on_new_status(self, blockchain_length, host, port):
        self.Status_Handler.handle_status_update(blockchain_length, host, port)


if __name__ == '__main__':
    args = update_config_from_args(sys.argv)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

MiningServer().start()
