#!/usr/bin/env python3
# -*- coding: utf-8 -*-

config = {
    'difficulty' : 5,
    'block_size' : 10,
   # 'block_reward' : 10,
    'mined_root_store' : 'mined_root_store.json',
    'key_store_dir' : '.',
    'key_format' : 'pem',
    'key_size' : 1024,
    'blockchain_store' : 'blockchain.json',
    'producer_blockchain_store' : 'producer_chain.json',
    'genesis_block_id' : 0,
    'network_broadcast_interval_seconds' : 20,
    'transaction_broadcast_interval_seconds' : 15,
    'Network_Broadcast_Port' : 3606,
    'Chain_Synchronization_port' : 3605,
    'transaction_port' : 3608,
    'Network_Listener_port' : 3609,
    #'Chain_Synchronization_listen' : 2605
}


def update_config_from_args(args):
    other_args = []
    for arg in args:
        k, v = arg.split('=') if '=' in arg else (None,None)
        if k in config:
            if isinstance(config[k], int):
                config[k] = int(v)
            else:
                config[k] = v
        else:
            other_args.append(arg)

    return other_args
