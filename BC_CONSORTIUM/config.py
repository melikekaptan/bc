#!/usr/bin/env python3

config = {
    'difficulty' : 4,
    'block_size' : 5,
    'key_store_dir' : '.',
    'key_format' : 'pem',
    'key_size' : 1024,
    'blockchain_store' : 'blockchain.json',
    'genesis_block_id' : 0,
    'Network_Broadcast_interval_seconds' :10 ,
    'transaction_broadcast_interval_seconds' : 5,
    'Network_Broadcast_port' : 2606,
    'Chain_Synchronization_port' : 2605,
    'transaction_port' : 2608,
    'Network_Listener_port' : 2609,
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
