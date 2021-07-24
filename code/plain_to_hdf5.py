#!/usr/bin/env python3
import os
import sys

import numpy as np
import calamardo
import skimage.io as imgio
from PIL import Image

if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit(1)
    din = sys.argv[1]

    images = [f for f in os.listdir(din) if os.path.isfile(os.path.join(din, f)) and f[-3:].lower() == 'tif' ]
    #images = [f for f in os.listdir(din) if os.path.isfile(os.path.join(din, f)) ]
    #
    # count records
    #
    n = len(images)
    cfout = calamardo.CalamariFile(sys.argv[2],'w',max_samples=n)
    invalid = 0
    for i,f in enumerate(images):
        imgfname = os.path.join(din,f)
        txtfname = os.path.join(din,f[:-3]+'gt.txt')
        #img = imgio.imread(imgfname)
        img = Image.open(imgfname)
        Ibool = np.array(img)
        I8 = np.zeros(Ibool.shape)
        I8[Ibool] = 255
        with open(txtfname,'r') as f:
            txt = f.readline().strip()
            if cfout.write(I8,txt) != 0:
                invalid += 1
        if i > 0 and not i % 100:
            print(f'{i:08d}/{n:08d}')
    print('total',n,'valid',n-invalid,'invalid',invalid)
    cfout.close()

