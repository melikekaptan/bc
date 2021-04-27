#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 23:45:48 2019

@author: melike
"""

import merkletools

mt = merkletools.MerkleTools()  # default is sha256 


hex_data1 = '05ae04314577b2783b4be98211d1b72476c59e9c413cfb2afa2f0c68e0d93911'
hex_data2 = '05aa04314577b2783b4be98211d1b72476c59e9c413cfb2afa2f0c68e0d93911'
hex_data3 = '05ai04314577b2783b4be98211d1b72476c59e9c413cfb2afa2f0c68e0d93911'
hex_data3 = '05a604314577b2783b4be98211d1b72476c59e9c413cfb2afa2f0c68e0d93911'
hex_data4 = '05ae14314577b2783b4be98211d1b72476c59e9c413cfb2afa2f0c68e0d93911'
hex_data5 = '05ae24314577b2783b4be98211d1b72476c59e9c413cfb2afa2f0c68e0d93911'
hex_data6 = '05ae34314577b2783b4be98211d1b72476c59e9c413cfb2afa2f0c68e0d93911'

mt.add_leaf(hex_data1)
mt.add_leaf(hex_data2)
mt.add_leaf(hex_data3)
mt.add_leaf(hex_data4)
mt.add_leaf(hex_data5)
mt.add_leaf(hex_data6)

#Generates the merkle tree using the leaves that have been added.
leaf_count =  mt.get_leaf_count();
print(leaf_count)
mt.make_tree();
root_value = mt.get_merkle_root();
print(root_value)