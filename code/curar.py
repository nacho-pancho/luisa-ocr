#!/usr/bin/env python3
import os
import sys
import subprocess
import tkinter as tk
import tkinter.font as tkfont

EXT='jpg'
FONTSIZE=16
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


def text_down(ev):
    global tkentry,dirtytext
    if ev.keysym == "Return":
        if len(dirtytext) > 0:
            # text has been modified
            data[index] = (data[index][0], dirtytext, data[index][2], True)
            refresh()

def text_up(ev):
    global dirtytext
    dirtytext = tkentry.get()
    print('dertey',dirtytext)


def refresh():
    global tkimg,tktxt,tkentry,dirtytext
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

    for i,d in enumerate(data):
        ipath,txt,deleted,modified = d
        path, iname = os.path.split(ipath)
        basename, ext = os.path.splitext(iname)
        tname = os.path.join(din, basename + '.gt.txt')

        if deleted:
            print('item ',i,'will be deleted')
            print('path',ipath,'text',txt)
            # BACKUP
            ibak = os.path.join(dout, iname)
            tbak = os.path.join(dout, basename + '.gt.txt')
            subprocess.run(['cp',ipath,ibak])
            subprocess.run(['cp', tname, tbak])
            # DELETE
            subprocess.run(['rm','-f',ipath])
            subprocess.run(['rm','-f',tname])

        elif modified:
            print('item',i,'will be modified')
            print('path', ipath, 'text', txt)
            # BACKUP
            ibak = os.path.join(dout, iname)
            tbak = os.path.join(dout, basename + '.gt.txt')
            subprocess.run(['cp',ipath,ibak])
            subprocess.run(['cp', tname, tbak])
            # MODIFY
            with open(tname,'w') as f:
                print(txt,file=f)

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

    images = sorted([f for f in os.listdir(din) if os.path.isfile(os.path.join(din, f)) and f[-3:].lower() == EXT ])
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


    txtfont = tkfont.Font(family="Helvetica",size=FONTSIZE)
    tkentry = tk.Entry(win,font=txtfont,width=80,borderwidth=5)
    tktxt = tk.StringVar(win,txt)
    tktxt.set(txt)
    tkentry['textvariable'] = tktxt
    tkentry.bind("<KeyPress>",text_down)
    tkentry.bind("<KeyRelease>",text_up)
    tkentry.pack()

    img = image=tk.PhotoImage(file=data[index][0])
    tkimg = tk.Label(win,image=img)
    tkimg.image = img
    tkimg.pack()

    tknote = tk.Label(win,text='unchanged',font=txtfont)
    tknote.pack()
    refresh()

    win.mainloop()
    for i,d in enumerate(data):
        if d[2]:
            print('item',i,'deleted')
        elif d[3]:
            print('item',i,'modified')
