from threading import Event
import signal, sys
import logging
from blockchain_loader_from_producer import ProducerBlockchainLoader
from Device_Listener import DeviceListener
from send import SendCommand
from crypto import Crypto

KEY_NAME = 'GW1234'
SERVICE_NAME = 'GATEWAY'
class Gateway:
    def __init__(self):
        self.shutdown_event = Event()
        ##load blockchain producer
        ##ask a device about its identity and version of the image
        ##check whether its a last version or not tracing the chain 
        self.Device_Listener = DeviceListener(4646, self.shutdown_event, self._get_device_info)
        crypto = Crypto()
        key = crypto.get_key(KEY_NAME) or crypto.generate_key(KEY_NAME)
        self.sender = key
    
    def _quit(self):
        logging.info("Stopping...")
        self.shutdown_event.set()
        self.Device_Listener.close() 
        
    def start(self):
        signal.signal(signal.SIGINT, self._quit)
        self.Device_Listener.start() 
        
    def _load_producer_blockchain(self):
        
        blockchain_stable = ProducerBlockchainLoader()._load()
        
        return blockchain_stable
    
    def _get_device_info(self, device_no, version):
        
        self._check_device_version(device_no, version)

    
    
    def _check_device_version(self, device_no, version):
        
        blockchain = self._load_producer_blockchain()
        print(type(blockchain.chain))
        list_chain = blockchain.chain
        
        device_history = dict()
        device_history[device_no] = []
        for block in blockchain.chain:
            print(block.id)
            for transactions in block.transactions:
                device_attr = str(transactions.model)
                if device_no.startswith(device_attr):
                    device_history[device_no].append(transactions.ipfs_doc)
                    #last_version = transaction.ipfs_doc
                    
        print(device_history)
        list_of_versions = device_history[device_no]
        if list_of_versions is not None:
            if version != list_of_versions[-1]:
                logging.info('{} detected a device need to be updated'.format(SERVICE_NAME))
              
                SendCommand(KEY_NAME, list_of_versions[-1], device_no)
                        


if __name__ == '__main__':
    #args = update_config_from_args(sys.argv)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

Gateway().start()    