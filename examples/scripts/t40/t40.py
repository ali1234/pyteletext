#!/usr/bin/env python

# Downloads the magazine from teletext40.com

import urllib2
import os
import sys
import shutil

if __name__=='__main__':
    outdir = 'data'

    outpath = os.path.join('.', outdir)
    if not os.path.isdir(outpath):
        os.makedirs(outpath)

    response = urllib2.urlopen('http://teletext40.com/data/frames.csv')
    #response = open('frames.csv', 'U')

    for line in response:
        tmp = line.strip().split(',')
        if len(tmp) != 4:
            continue
        page = int(tmp[0], 16)
        subpage = int(tmp[1], 16)
        data = tmp[3].decode('hex')
        pagedir = os.path.join(outpath, '%03x' % page)
        if not os.path.isdir(pagedir):
            os.makedirs(pagedir)
        subpage_filename = os.path.join(pagedir, '%04x.tt' % subpage)
        subpage_file = open(subpage_filename, 'wb')
        subpage_file.write('\x00'*64) # no header info available
        subpage_file.write(data[40:])
        subpage_file.write(data[:40]) # line 25 is at the top?
        subpage_file.write('\x00'*52) # no flof available
        subpage_file.close()
