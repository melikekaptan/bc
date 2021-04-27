import socket
from threading import Thread
from threading import Event
from utils import bytes_to_text
import logging
import sys
import signal, sys
from config import config

SERVICE_NAME = 'Device Listener'
BUFFER_SIZE = 1024 * 1024
BACKLOG_SIZE = 5

device_list = [('1234567890100001', 'B640E840B19D378660B32FB51AE18D67DCCB4A8596A29E7BD72C1B2AE5928F41'),
               ('1234567890103912', '16367AACB67A4A017C8DA8AB95682CCB390863780F7114DDA0A0E0C55644C7C4'),
               ('1234567890203932',' 5EEF8098ED6EC0A16249FC7C12422027FC9FD75B16130CC9382CF09102014796'),
               ('1234567890203992', 'D9A96B71E029CE34DEF0DC8C4DDF6B97A661BDEE2F814B34FCB365185FC855E4'),
               ('1234567890293992', '58C4A1F7C2221CCCDCFDFEE436ECDDAF353263A289DB1EDDAA34C848153D8476'),
               ('1234567890123933', 'D6ED5AF4961AEFA3953AF0047309D9B660D9BB0D468D6529B4ABB8829B54AC2F'),
               ('1234567890123933', 'D6ED5AF4961AEFA3953AF0047309D9B660D9BB0D468D6529B4ABB8829B54AC2F'),
               ('1234567890123933', 'E6ED5AF4961AEFA3953AF0047309D9B660D9BB0D468D6529B4ABB8829B54AC2F'),
               ('1234567890123933', 'F6ED5AF4961AEFA3953AF0047309D9B660D9BB0D468D6529B4ABB8829B54AC2F'),
               ('1234587890122933', '76ED5AF4961AEFA3953AF0047309D9B660D9BB0D468D6529B4ABB8829B54AC2F'),
               ('1234587890122933', '86ED5AF4961AEFA3953AF0047309D9B660D9BB0D468D6529B4ABB8829B54AC2F'),
               ('1234587890122933', '96ED5AF4961AEFA3953AF0047309D9B660D9BB0D468D6529B4ABB8829B54AC2F'),
               ('1234567890122933', '06ED5AF4961AEFA3953AF0047309D9B660D9BB0D468D6529B4ABB8829B54AC2F'),
               ('1234577890122933', '16ED5AF4961AEFA3953AF0047309D9B660D9BB0D468D6529B4ABB8829B54AC2F'),
               ('1234577890122933', '26ED5AF4961AEFA3953AF0047309D9B660D9BB0D468D6529B4ABB8829B54AC2F')]

class DeviceListener(Thread):
    def __init__(self, listener_port, shutdown_event, _get_device_info):
        Thread.__init__(self)
        self.shutdown_event = shutdown_event
        self.listener_port = listener_port
        self._get_device_info = _get_device_info
        self.broadcast_interval_seconds = config.get('transaction_broadcast_interval_seconds')

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', self.listener_port))
        logging.info('{} listening for device on port {}...'.format(SERVICE_NAME, self.listener_port))
      
        while not self.shutdown_event.is_set():
            
            for elem in device_list:
                self.shutdown_event.wait(self.broadcast_interval_seconds)
                try:
                    logging.info('{} received new status update from device'.format(SERVICE_NAME))
                    device_no, version = elem
                    logging.info('{} received new status update of {} from {}'.format(SERVICE_NAME, version, device_no, ))
                    self._get_device_info(device_no, version)
        
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
        
        
        
