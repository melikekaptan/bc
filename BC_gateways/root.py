import logging


class RootMiner:
    def __init__(self):
        self.root_chain = []
    
    def add_root(self,root_element):
        self.root_chain.append(root_element)
    
    def has_transaction_with_same_update_for_same_device(self, transaction):
        return any(map(lambda b : b.has_transaction_with_same_update_for_same_device(transaction), self.root_chain))
    
    
class RootElement:
    def __init__(self):
        self.transaction_root = None
        self.transactions = []
        
    def has_transaction_with_same_update_for_same_device(self, transaction):
        return next((True for t in self.transactions if t['ipfs_doc'] == transaction.ipfs_doc and t['model'] == transaction.model), False)
