class TransactionProducer:
    def __init__(self, from_address, ipfs_doc, model, public_key):
        self.from_address = from_address
        self.ipfs_doc = ipfs_doc
        self.model = model
        self.public_key = public_key
        self.timestamp = None
        self.id = None
        self.signature = None

    def get_details_for_signature(self):
        return '{} {} {} {}'.format(self.from_address, str(self.ipfs_doc), self.model, self.timestamp)

    def __repr__(self):
        return '{} --[{}]--> {}'.format(self.from_address, str(self.ipfs_doc), self.model)