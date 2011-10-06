#!/usr/bin/env python

# Google PageRank Checksum Algorithm (Internet Explorer Toolbar)
#	Downloaded from http://pagerank.phurix.net/

# Settings
prhost='toolbarqueries.google.com'
prurl='http://%s/tbr?client=navclient-auto&ch=%s&features=Rank&q=info:%s'

# Definitions
def  IntStr(String, Integer, Factor):
    for i in range(len(String)) :
        Integer *= Factor
        Integer &= 0xFFFFFFFF
        Integer += ord(String[i])
    return Integer


def HashURL(Str):
    C1 = IntStr(Str, 0x1505, 0x21)
    C2 = IntStr(Str, 0, 0x1003F)

    C1 >>= 2
    C1 = ((C1 >> 4) & 0x3FFFFC0) | (C1 & 0x3F)
    C1 = ((C1 >> 4) & 0x3FFC00) | (C1 & 0x3FF)
    C1 = ((C1 >> 4) & 0x3C000) | (C1 & 0x3FFF)

    T1 = (C1 & 0x3C0) << 4
    T1 |= C1 & 0x3C
    T1 = (T1 << 2) | (C2 & 0xF0F)

    T2 = (C1 & 0xFFFFC000) << 4
    T2 |= C1 & 0x3C00
    T2 = (T2 << 0xA) | (C2 & 0xF0F0000)

    return (T1 | T2)


def CheckHash(HashInt):
    HashStr = "%u" % (HashInt)
    Flag = 0
    CheckByte = 0

    i = len(HashStr) - 1
    while i >= 0:
        Byte = int(HashStr[i])
        if 1 == (Flag % 2):
            Byte *= 2;
            Byte = Byte / 10 + Byte % 10
        CheckByte += Byte
        Flag += 1
        i -= 1

    CheckByte %= 10
    if 0 != CheckByte:
        CheckByte = 10 - CheckByte
        if 1 == Flag % 2:
            if 1 == CheckByte % 2:
                CheckByte += 9
            CheckByte >>= 1

    return '7' + str(CheckByte) + HashStr


def GetURL():
	hash = CheckHash(HashURL(query))
	url = prurl % (prhost,hash,query)
	return url

#EOF