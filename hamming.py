# Hamming and parity calculations
# Copyright 2009-2015 Alistair Buxton <a.j.buxton@gmail.com>

# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

def hamming84(d):
    d1 = d&1
    d2 = (d>>1)&1
    d3 = (d>>2)&1
    d4 = (d>>3)&1

    p1 = (1 + d1 + d3 + d4) & 1
    p2 = (1 + d1 + d2 + d4) & 1
    p3 = (1 + d1 + d2 + d3) & 1
    p4 = (1 + p1 + d1 + p2 + d2 + p3 + d3 + d4) & 1

    return (p1 | (d1<<1) | (p2<<2) | (d2<<3) 
     | (p3<<4) | (d3<<5) | (p4<<6) | (d4<<7))

def parity(d):
    d &= 0x7f
    p = 1
    t = d
    for i in range(7):
        p += t&1
        t = t>>1
    p &= 1
    return d|(p<<7)

if __name__ == '__main__':
    for n in range(16):
        print n, hamming84(n)

