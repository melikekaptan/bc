#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from crypto import Crypto
import logging

KEY_STORE_DIR = '.'



class MakeAddress:

    def __init__(self, *args):
        if len(args) != 1:
            logging.error('wrong number of args for {}'.format(MakeAddress))

        else:
            key_name = args[0]
            try:
                key = Crypto().generate_key(key_name)
                logging.info('Generated key [{}] with address {}. Key saved in {}'.format(key.name, key.address, key.key_file_path))
            except BaseException as e:
                logging.error(e)
                
    
 
