# Copyright 2009-2015 Alistair Buxton <a.j.buxton@gmail.com>

# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

from hamming import hamming84, parity


def page_subpage(page=0xff, subpage=0, control=0):
    p = chr(hamming84(page&0xf)) + chr(hamming84(page>>4))
    p += chr(hamming84((subpage)&0xf)) + chr(hamming84(((subpage>>4)&0x7)|((control&1)<<3)))
    p += chr(hamming84((subpage>>8)&0xf)) + chr(hamming84(((subpage>>12)&0x3)|((control&6)<<1)))
    return p

def page_subpage_full(page=0xff, subpage=0, control=0):
    return page_subpage(page, subpage, control) + chr(hamming84((control>>3)&0xf)) + chr(hamming84((control>>7)&0xf))

def packet_830():
    """Common packet run in and magazine/address code, common to all packet types."""
    packet = chr(hamming84(0)) + chr(hamming84(30>>1))
    packet += chr(hamming84(0)) + page_subpage(0, 0x3f7f, 1)
    packet += chr(hamming84(20)) * 13
    for c in "Linux               ":
        packet += chr(parity(ord(c)))
    return packet

