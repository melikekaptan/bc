#!/usr/bin/env python3

class Transaction:
    def __init__(self, from_gateway, ipfs_doc, model, public_key):
        self.from_gateway = from_gateway
        self.ipfs_doc = ipfs_doc
        self.model = model
        self.public_key = public_key
        self.timestamp = None
        self.id = None
        self.signature = None

    def get_details_for_signature(self):
        return '{} {} {} {}'.format(self.from_gateway, str(self.ipfs_doc), self.model, self.timestamp)

    def __repr__(self):
        return '{} --[{}]--> {}'.format(self.from_gateway, str(self.ipfs_doc), self.model)
    
    
