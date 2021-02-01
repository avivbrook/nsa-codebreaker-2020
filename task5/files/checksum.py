def checksum(string):
    c = 0
    for s in string:
        c ^= ord(s)
    return c
