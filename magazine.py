# Magazine class, hold a carousel of pages
# Copyright 2009-2015 Alistair Buxton <a.j.buxton@gmail.com>

# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

import datetime, sys

from page import Page
from hamming import hamming84, parity
from packet import *

class Magazine(object):
    def __init__(self, number, title="Teletext"):
        self.pages = [None]*256
        if number == 0: 
            number = 8
        self.number = number
        self.title = title
        self.current_page = 0

    def add_page(self, number, src):
        sys.stderr.write("adding page %d, %d\n" % (self.number, number))
        self.pages[number] = Page(self.number, number, src)

    def del_page(self, number):
        sys.stderr.write("deleting page %d %d\n" % (self.number, number))
        self.pages[number] = None

    def packet_start(self, page, address):
        """Common packet run in and magazine/address code, common to all packet types."""
        return chr(hamming84(self.number|((address&1)<<3))) + chr(hamming84(address>>1))

    def header(self, page=0xff, subpage=0, control=0):
        """Page header packet, typically showing MPAG, magazine name, and date/time."""
        packet = self.packet_start(page, 0)
        packet += page_subpage_full(page, subpage, control)

        data = self.title
        data += " "+str(self.number)+(hex(page)[2:].zfill(2))
        t = datetime.datetime.now()
        data += t.strftime(" %a %d %b\x03%H:%M/%S")
        data += chr(0)*(32-len(data))

        for i in range(32):
            packet += chr(parity(ord(data[i])))
        
        return packet

    def next_page_packets(self):
        """Returns a list of the packets which must be sent for the next page in the carousel (for this magazine.)"""
        lines = []
        i = 1
        while self.pages[(self.current_page+i)%256] == None and i <= 256:
            i += 1

        if i > 0:
            self.current_page += i
            self.current_page %= 256

        if self.pages[self.current_page]:
            p = self.pages[self.current_page]
            (l,f,c) = p.data()

            lines.append(self.header(self.current_page, p.current_subpage, c))
            for d in range(len(l)):
                lines.append(self.packet_start(self.current_page, d+1)+l[d])

            lines.append(self.packet_start(self.current_page, 27)+f)

        return lines
