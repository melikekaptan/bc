#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from transaction import Transaction
from hash import hash_string_to_hex
#import time
import datetime

def build_transaction(from_gateway, ipfs_doc, model, key):
    transaction = Transaction(from_gateway, ipfs_doc, model, key.get_public_key())
    #transaction.timestamp = int(time.time() * 1000)
    transaction.timestamp = str(datetime.datetime.now())
    transaction_data_to_sign = transaction.get_details_for_signature()
    transaction.signature = key.sign(transaction_data_to_sign)
    transaction.id = hash_string_to_hex(str(transaction.signature))

    return transaction
