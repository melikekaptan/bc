from root import RootMiner
from root import RootElement
from encoders import rootchain_encode, rootchain_decode
import os.path
import logging
from threading import Lock
from config import config

class MinedRootLoader:
    lock = Lock()

    def __init__(self, location = None):
        self.mined_root_store = location or config.get('mined_root_store')

    def _load(self):
        if os.path.isfile(self.mined_root_store):
            root_records = rootchain_decode(open(self.mined_root_store).read())
            print('GATEWAY: Loaded {} blocks from {} '.format(len(root_records.root_chain), self.mined_root_store))
            return root_records
        else:
            root_records = RootMiner()
            root_records.root_chain = []
            return root_records

    def _save(self, root_records):
        open(self.mined_root_store, 'w').write(rootchain_encode(root_records))

    def process(self, op):
        MinedRootLoader.lock.acquire()
        try:
            root_records = self._load()
            result = op(root_records)
            self._save(root_records)
            return result
        finally:
            MinedRootLoader.lock.release()
