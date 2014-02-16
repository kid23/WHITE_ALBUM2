#For WHITE ALBUM2 PS3 File Script
#By KiD

import mmap
import os
import struct
import sys
import codecs

def make_tbl(buf, size, name):
    cur = 0
    out = codecs.open(name, "wb+", encoding="utf-16")
    #out = open(name, "wb+")
    cnt = 0
    while cur < size :
        t1 = struct.unpack("<B", buf[cur:cur+1])
        t2 = struct.unpack("<B", buf[cur+1:cur+2])
        if (t1[0] < 0x80) :
            code = "%x=%c\r\n" % (t1[0], buf[cur:cur+1])
        else:
            code = "%x%x=%s\r\n" % (t1[0], t2[0], buf[cur:cur+2])
        out.write(unicode(code,'cp932'))
        cur += 2
        cnt += 1
    out.close()
    print "Total %d char." % cnt

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Bad argv.')
        sys.exit(0)

    fd = os.open(sys.argv[1], os.O_RDONLY)
    size = os.fstat(fd).st_size
    #buf = mmap.mmap(fd, size, prot=mmap.PROT_READ)
    buf = mmap.mmap(fd, size, access=mmap.ACCESS_READ)
    make_tbl(buf, size, sys.argv[2])
    os.close(fd)
