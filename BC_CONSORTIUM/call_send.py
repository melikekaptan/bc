#!/usr/bin/env python3
from send import SendCommand
import os
import time

myCmd = 'ipfs add mytextfile.txt > out.txt'
os.system(myCmd)
f = open("out.txt", "r").read()
lst = f.split()
#print(lst[1])
hashed_content = lst[1]
#SendCommand("sender1", hashed_content , "model 333")
SendCommand('Sender6', hashed_content, '12345')

time.sleep(1)

myCmd1 = 'ipfs add mytextfile1.txt > out1.txt'
os.system(myCmd1)
f1 = open("out1.txt", "r").read()
lst1 = f1.split()
#print(lst1[1])
hashed_content1 = lst1[1]
SendCommand("Sender1", hashed_content1, "12345")

time.sleep(1)

myCmd2 = 'ipfs add mytextfile2.txt > out2.txt'
os.system(myCmd2)
f2 = open("out2.txt", "r").read()
lst2 = f2.split()
#print(lst2[1])
hashed_content2 = lst2[1]
SendCommand("Sender2", hashed_content2, "12345")

time.sleep(1)

myCmd3 = 'ipfs add mytextfile3.txt > out3.txt'
os.system(myCmd3)
f3 = open("out3.txt", "r").read()
lst3 = f3.split()
#print(lst3[1])
hashed_content3 = lst3[1]
SendCommand("Sender3", hashed_content3, "12345")

time.sleep(1)

myCmd4 = 'ipfs add mytextfile4.txt > out4.txt'
os.system(myCmd4)
f4 = open("out4.txt", "r").read()
lst4 = f4.split()
#print(lst4[1])
hashed_content4 = lst4[1]
SendCommand("Sender4", hashed_content4, "12345")

time.sleep(1)

myCmd5 = 'ipfs add mytextfile5.txt > out5.txt'
os.system(myCmd5)
f5 = open("out5.txt", "r").read()
lst5 = f5.split()
#print(lst5[1])
hashed_content5 = lst5[1]
SendCommand("Sender5", hashed_content5, "12345")

time.sleep(1)

myCmd6 = 'ipfs add mytextfile6.txt > out6.txt'
os.system(myCmd6)
f6 = open("out6.txt", "r").read()
lst6 = f6.split()
#print(lst6[1])
hashed_content6 = lst6[1]
SendCommand("Sender6", hashed_content6, "12345")


















