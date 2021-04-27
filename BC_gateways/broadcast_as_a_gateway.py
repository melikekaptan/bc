from threading import Thread
from threading import Event
import socket
from utils import text_to_bytes
import logging
import signal, sys
from blockchain_loader import BlockchainLoader
from config import update_config_from_args


SERVICE_NAME = 'Gateway Broadcaster'
BROADCAST_ADDRESS = '255.255.255.255'

class GatewayBroadcaster(Thread):
    def __init__(self, broadcast_port, Chain_Synchronization_port, broadcast_interval_seconds):
        Thread.__init__(self)
        self.shutdown_event = Event()
        self.broadcast_port = broadcast_port
        self.Chain_Synchronization_port = Chain_Synchronization_port
        self.broadcast_interval_seconds = broadcast_interval_seconds
    def run(self):
        logging.info('{} started sending to port {}...'.format(SERVICE_NAME, self.broadcast_port))
        while not self.shutdown_event.is_set():
            self._broadcast_status()
            self.shutdown_event.wait(self.broadcast_interval_seconds)
           
        logging.info('{} shut down'.format(SERVICE_NAME))
        
        
    def _broadcast_status(self):
        
        while not self.shutdown_event.is_set():
            try:
                blockchain_length = self._get_blockchain_status_value()
                status_message_bytes = text_to_bytes('{}:{}'.format(blockchain_length, self.Chain_Synchronization_port))
                print('Gateway Broadcaster status message is ready to send')
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                s.sendto(status_message_bytes, (BROADCAST_ADDRESS, self.broadcast_port))
                print("sent status message")
                s.close()
                logging.info('{} sent {}.'.format(SERVICE_NAME, 'hello_from_GW1'))
                self._new_blocks_on_the_chain(blockchain_length, host, port)
            except:
                print('exeption')
        logging.info('{} shut down'.format(SERVICE_NAME))

    def _quit(self, signal, frame):
        logging.info("Stopping...")
        self.shutdown_event.set()
        
    def _get_blockchain_status_value(self):
        return BlockchainLoader().process(lambda blockchain : len(blockchain.chain))      
    #def start(self):
    #    signal.signal(signal.SIGINT, self._quit)            
     #   self.shutdown_event.wait()
      #  logging.info("Main thread stopped")
        
if __name__ == '__main__':
    args = update_config_from_args(sys.argv)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


        
