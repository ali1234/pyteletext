#!/usr/bin/env python

# This is the main stuff. Gets the binary page data 
# and turns it to a bitmap and draws it on a loop (carousel)

# Copyright 2009-2015 Alistair Buxton <a.j.buxton@gmail.com>

# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

from hamming import *
from magazine import Magazine
from packet import *

import os
import random
import datetime

import gamin
import time
import sys

src_dir = sys.argv[1]
m = []
for i in range(0,8):
    m.append(Magazine(i, "Teletext"))

def file_changed(path, event):
    if len(path) == 3:
        try:
            mag = int(path[0])&7
            page = int(path[1:3], 16)
            if event == 5 or event == 8:
                m[mag].add_page(page, src_dir+'/'+path)
            elif event == 2 or event == 3:
                m[mag].del_page(page)
        except ValueError:
            pass

def main():


    running = 1
    n = 0
    p = 0

    cm = 0

    packet_list = []

    mon = gamin.WatchMonitor()
    mon.watch_directory(src_dir, file_changed)

    while running:

        if len(packet_list) > 0:
            p = packet_list.pop(0)
            for i in range(1):
                sys.stdout.write(p)

        while len(packet_list) == 0:
            cm += 1
            cm %= len(m)
            packet_list = m[cm].next_page_packets()
            if cm == 0:
                packet_list.append(packet_830())

        ret = mon.event_pending()
        if ret > 0:
            ret = mon.handle_one_event()

        time.sleep(0.001)




if __name__ == '__main__': main()
