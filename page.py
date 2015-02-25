# Page class
# Copyright 2009-2015 Alistair Buxton <a.j.buxton@gmail.com>

# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

import os
from struct import unpack

from hamming import *
from packet import *

class SubPage(object):

    def __init__(self, magazine, number, src):
        self.lines = []
        self.magazine = magazine
        self.number = number

        data = file(src, 'rb').read()

        f = 64
        for l in range(24):
            line = ""
            for c in data[f:f+40]:
                line += chr(parity(ord(c)))
            self.lines.append(line)
            f+=40

        tmp = unpack("i"*12, data[f+4:f+52])
        #print self.magazine, self.number
        self.flof = chr(hamming84(0))
        for i in range(0,12,2):
            #print hex(tmp[i]), hex(tmp[i+1]), hex(self.magazine^(tmp[i]>>8))
            self.flof += page_subpage(tmp[i]&0xff, tmp[i+1], self.magazine^(tmp[i]>>8))
        self.flof += chr(hamming84(0xf))
        self.flof += "  "
        tmpo = unpack("i", data[12:16])

        tmp = tmpo[0]
        self.control = ((tmp&0x1f)<<3)|((tmp&0xe0)>>5)

class Page(object):

    def __init__(self, magazine, number, src):
        self.subpages = []
        self.current_subpage = 0
        self.magazine = magazine
        self.number = number
        subs = os.listdir(src)
        subs.sort()
        for tt in subs:
            self.subpages.append(SubPage(self.magazine, self.number, src+'/'+tt))

    def data(self):
        sp = self.subpages[self.current_subpage]
        self.current_subpage += 1
        self.current_subpage %= len(self.subpages)
        return (sp.lines, sp.flof, sp.control)

