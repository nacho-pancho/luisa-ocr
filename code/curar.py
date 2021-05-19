#!/usr/bin/env python3
import os
import sys

import numpy as np
import calamardo
import skimage.io as imgio
from PIL import Image
import tkinter as tk
import tkinter.font as tkfont


index = 0
nimages = 0 
data = list()
tkimg = None
tktxt = None
tknote = None

def key_handler(e):
    if e.keysym == 'Left':
        go_to_prev()
    elif e.keysym == 'Right':
        go_to_next()    
    elif e.keysym == 'Delete':
        delete_entry()

def go_to_next():
    print('next')
    global index
    global nimages
    if index < (nimages - 1):
        index += 1    
        refresh()

def go_to_prev():
    print('prev')
    global index
    while index > 0:
        index -= 1
        refresh()

def delete_entry():
    data[index] = (data[index][0],data[index][1],True,data[index][3])
    print('delete')
    refresh()

def refresh():
    print("refresh")
    img = tk.PhotoImage(file=data[index][0])
    tkimg.image    = img
    tkimg['image'] = img
    tktxt['text']  = data[index][1]
    if data[index][2]:
        tknote['text'] = 'deleted'
        tknote['fg'] = 'red'
    elif data[index][3]:
        tknote['text'] = 'modified'
        tknote['fg'] = 'orange'
    else:
        tknote['text'] = 'unchanged'
        tknote['fg'] = 'green'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(1)
    din = sys.argv[1]
    
    images = sorted([f for f in os.listdir(din) if os.path.isfile(os.path.join(din, f)) and f[-3:].lower() == 'gif' ])
    nimages = len(images)
    for i,f in enumerate(images):
        imgfname = os.path.join(din,f)
        txtfname = os.path.join(din,f[:-3]+'gt.txt')
        with open(txtfname,'r') as f:
            txt = f.readline().strip()
        # image name, text, to be deleted, to be modified
        data.append((imgfname,txt,False,False)) 
        if i > 0 and not i % 1000:
            print(f'{i:08d}/{nimages:08d}')
    #
    # interface
    #
    win = tk.Tk()
    win.bind('<KeyPress>',key_handler)

    txtfont = tkfont.Font(family="Helvetica",size=12)
    tktxt = tk.Label(win,text=data[index][1],font=txtfont)
    tktxt.pack()

    img = image=tk.PhotoImage(file=data[index][0])
    tkimg = tk.Label(win,image=img)
    tkimg.image = img
    tkimg.pack()

    tknote = tk.Label(win,text='unchanged',font=txtfont)
    tknote.pack()

    win.mainloop()
    for i,d in enumerate(data):
        if d[2]:
            print('item',i,'deleted')
        elif d[3]:
            print('item',i,'modified')
