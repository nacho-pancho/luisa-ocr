#!/usr/bin/env python3
import os
import sys
import subprocess

import tkinter as tk
import tkinter.font as tkfont


index = 0
nimages = 0 
data = list()
tkimg = None
tktxt = None
tkentry = None
tknote = None
dirtytext = ""

def key_handler(e):
    if e.keysym == 'Up':
        go_to_prev()
    elif e.keysym == 'Down':
        go_to_next()
    elif e.keysym == 'F4':
        delete_entry()
    elif e.keysym == 'F2':
        apply()
    elif e.keysym == 'Escape':
        quit()
    else:
        print('???')

def go_to_next():
    global index
    global nimages
    if index < (nimages - 1):
        index += 1    
        refresh()

def go_to_prev():
    global index
    if index > 0:
        index -= 1
        refresh()

def delete_entry():
    data[index] = (data[index][0],data[index][1],True,data[index][3])
    refresh()

def edit_text(ev):
    global tkentry,dirtytext
    if ev.keysym == "Return":
        if len(dirtytext) > 0:
            # text has been modified
            data[index] = (data[index][0], dirtytext, data[index][2], True)
            refresh()
    else:
        dirtytext = tkentry.get()  + ev.char
        print(dirtytext)

def refresh():
    global tkimg,tktxt,tkentry,dirtytext
    print("refresh")
    img = tk.PhotoImage(file=data[index][0])
    tkimg.image    = img
    tkimg['image'] = img
    tktxt.set(data[index][1])
    tkentry['textvariable'] = tktxt

    if data[index][2]:
        tknote['text'] = 'deleted'
        tknote['fg'] = 'red'
    elif data[index][3]:
        tknote['text'] = 'modified'
        tknote['fg'] = 'orange'
    else:
        tknote['text'] = 'unchanged'
        tknote['fg'] = 'green'
    dirtytext =""

def apply():
    print('apply')
    for i,d in enumerate(data):
        ipath,txt,deleted,modified = d
        do_backup = False
        if deleted:
            print('item ',i,'will be deleted')
            print('path',ipath,'text',txt)
            do_backup = True
        elif modified:
            print('item',i,'will be modified')
            print('path', ipath, 'text', txt)
            do_backup = True

        if do_backup:
            path,iname = os.path.split(ipath)
            basename,ext = os.path.splitext(iname)
            ibak = os.path.join(dout,iname)
            tname  = os.path.join(din,basename+'.gt.txt')
            tbak = os.path.join(dout,basename+'.gt.txt')
            print("cp",ipath,ibak)
            print("cp",tname,tbak)
            subprocess.run(['cp',ipath,ibak])
            subprocess.run(['cp', tname, tbak])
    exit(0)

def quit():
    print('quit ')
    exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(1)
    din = sys.argv[1]
    if len(sys.argv) > 2:
        dout = sys.argv[2]
    else:
        dout = os.path.join(din,'backup')
    if not os.path.exists(dout):
        os.makedirs(dout,exist_ok=True)

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


    txtfont = tkfont.Font(family="Helvetica",size=14)
    #tktxt = tk.Label(win,text=data[index][1],font=txtfont)
    tktxt = tk.StringVar(win,txt)
    tkentry = tk.Entry(win,font=txtfont,width=80,borderwidth=5)
    tkentry.textvariable = tktxt
    tkentry.bind("<KeyPress>",edit_text)
    tkentry.pack()

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
