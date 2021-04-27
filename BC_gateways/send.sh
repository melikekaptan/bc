#!/bin/bash
#!/usr/bin/env/ python3

gnome-terminal --tab --title="test" --command="IPFS_PATH=~/.ipfs ipfs add file.txt; $SHELL"



chmod +x call_send.py
python call_send.py




