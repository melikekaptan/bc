import socket
from threading import Thread
from threading import Event
from utils import bytes_to_text
import logging
import sys
import signal, sys

SERVICE_NAME = 'Gateway Listener'
BUFFER_SIZE = 1024 * 1024
BACKLOG_SIZE = 5

class GatewayListener(Thread):
    def __init__(self, listener_port, shutdown_event, _on_new_gateway_status):
        Thread.__init__(self)
        self.shutdown_event = shutdown_event
        self.listener_port = listener_port
        self._on_new_gateway_status = _on_new_gateway_status

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', self.listener_port))
        print("socket bind")
        logging.info('{} listening for gateway list on port {}...'.format(SERVICE_NAME, self.listener_port))
      
        while not self.shutdown_event.is_set():
            
            try:
                print("new status update from GATEWAY")
                logging.info('{} received new status update from GATEWAY'.format(SERVICE_NAME))
                bytes, addr = self.socket.recvfrom(BUFFER_SIZE)
                print(addr)
                status_value, Chain_Synchronization_port = bytes_to_text(bytes).split(':')
                host = addr[0]
                print(host, int(Chain_Synchronization_port))
                logging.info('{} received new status update of {} from {}:{}'.format(SERVICE_NAME, status_value, host, Chain_Synchronization_port))
                self._on_new_gateway_status(int(status_value), host,  str(Chain_Synchronization_port))
    
            except OSError:
                logging.info('{} error; {}'.format(SERVICE_NAME, sys.exc_info()))
                pass # probably close() was called
    
            except Exception:
                logging.error('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))

        logging.info('{} shut down'.format(SERVICE_NAME))
        
    def _quit(self, signal, frame):
        logging.info("Stopping...")
        self.shutdown_event.set()

    def close(self):
        self.socket.close()
        
        
        

