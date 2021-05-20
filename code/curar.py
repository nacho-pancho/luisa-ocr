#!/usr/bin/env python3
import os
import sys
import subprocess
import tkinter as tk
import tkinter.font as tkfont
import argparse
from PIL import Image,ImageTk

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
    elif e.keysym == 'F6':
        undelete_entry()
    elif e.keysym == 'F4':
        delete_entry()
    elif e.keysym == 'F2':
        apply()
    elif e.keysym == 'F8':
        revert_entry()
    elif e.keysym == 'Escape':
        quit()

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


def undelete_entry():
    data[index] = (data[index][0],data[index][1],False,data[index][3])
    refresh()

def revert_entry():
    dirtytext = ""
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


def refresh():
    global tkimg,tktxt,tkentry,dirtytext

    img = Image.open(data[index][0])
    img = ImageTk.PhotoImage(img)
    tkimg.image    = img
    tkimg['image'] = img
    tktxt.set(data[index][1])
    tkentry['textvariable'] = tktxt
    #
    # text is name of image
    #
    _,basename = os.path.split(data[index][0])
    newtext = f'{basename} ({index:6d}/{nimages:6d})'

    if data[index][2]:
        tknote['text'] = newtext + ' **deleted]**'
        tknote['fg'] = 'red'
    elif data[index][3]:
        tknote['text'] = newtext + ' **modified**'
        tknote['fg'] = 'orange'
    else:
        tknote['text'] = newtext
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--font_size", type=int, default=12,
                    help="font size")
    ap.add_argument("--img_ext", type=str, default="gif",
                    help="image format extension")
    ap.add_argument("--text_ext", type=str, default="gt.txt",
                    help="ground truth text file extension")
    ap.add_argument("--bakdir", type=str, default="",
                    help="backup dir (defaults to 'backup' under source dir)")
    ap.add_argument("indir", type=str, help="source dir")
    args = vars(ap.parse_args())
    ext = args["img_ext"]
    txext = args["text_ext"]
    din = args["indir"]
    if len(args["bakdir"]):
        dout = args["bakdir"]
    else:
        dout = os.path.join(din,'backup')
    if not os.path.exists(dout):
        os.makedirs(dout,exist_ok=True)

    images = sorted([f for f in os.listdir(din) if os.path.isfile(os.path.join(din, f)) and f[-3:].lower() == ext ])
    index = 0
    nimages = len(images)
    if nimages == 0:
        print('no images found')
        exit(1)
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

    txtfont = tkfont.Font(family="Helvetica",size=args["font_size"])
    tkentry = tk.Entry(win,font=txtfont,width=80,borderwidth=5)
    tktxt   = tk.StringVar(win)
    tktxt.set(data[index][1])
    tkentry['textvariable'] = tktxt
    tkentry.bind("<KeyPress>",text_down)
    tkentry.bind("<KeyRelease>",text_up)
    tkentry.pack()
    img = Image.open(data[index][0])
    img = ImageTk.PhotoImage(img)
    tkimg = tk.Label(win,image=img)
    tkimg.image = img
    tkimg.pack()
    _,basename = os.path.split(data[index][0])
    tknote = tk.Label(win,text=f'{basename} ( {index:6d} / {nimages:6d} ) ',font=txtfont)
    tknote.pack()
    refresh()

    win.mainloop()
