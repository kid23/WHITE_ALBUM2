#For WHITE ALBUM2 PS3 File Script
#By KiD

import mmap
import os
import struct
import sys
import codecs
from sets import Set

def convert2unicode(buf, size, name):
    out = codecs.open(name, "wb+", encoding="utf-16")
    out.write(unicode(buf,'cp932'))
    out.close()

def load_tbl(name):
    TBL={}
    tbl_file = codecs.open(name, "r", encoding="utf-16")
    alllines = tbl_file.readlines()
    for eachline in alllines:
        if eachline[0] > u'7' :
            code = eachline[0:4]
            char = eachline[5:6]
            c = int(code, 16)
            TBL[char] = c
    tbl_file.close()
    print "Load %d char." % len(TBL)
    return TBL

def replace_txt(txtname,TBL,MISSED):
    fd = os.open(txtname, os.O_RDWR)
    size = os.fstat(fd).st_size
    buf = mmap.mmap(fd, size, access=mmap.ACCESS_WRITE)
    cur = 0
    left = 0
    while cur < size :
        t1 = struct.unpack("<B", buf[cur:cur+1])
        if t1[0] >= 0x80 :
            char = unicode(buf[cur:cur+2],'cp936')
            if TBL.has_key(char) :
                buf[cur:cur+2] = struct.pack(">H", TBL[char])
            else :
                left += 1
                MISSED.add(char)
            cur += 2
        else :
            cur += 1
    os.close(fd)
    if left > 0 :
        print 'replace %s.(left %d)' % (txtname, left)
    else :
        print 'replace %s ok.' % (txtname)

def batch_replace_txt(dir,name):
    TBL=load_tbl(name)
    MISSED=Set()
    for directory, subdirectories, files in os.walk(dir):
      for file in files:
        if file.endswith('.txt'):
            replace_txt(os.path.join(directory, file), TBL, MISSED)
    for val in MISSED :
        print val,
    
def make_tbl(buf, size, name):
    cur = 0
    tbl_file = codecs.open(name + ".tbl", "wb+", encoding="utf-16")
    txt_file = codecs.open(name + ".txt", "wb+", encoding="utf-16")
    cnt = 0
    while cur < size :
        t1 = struct.unpack("<B", buf[cur:cur+1])
        t2 = struct.unpack("<B", buf[cur+1:cur+2])
        if (t1[0] < 0x80) :
            code = "%x=%c\r\n" % (t1[0], buf[cur:cur+1])
            txt = buf[cur:cur+1]
        else:
            code = "%x%x=%s\r\n" % (t1[0], t2[0], buf[cur:cur+2])
            txt = buf[cur:cur+2]
        tbl_file.write(unicode(code,'cp932'))
        txt_file.write(unicode(txt,'cp932'))
        cur += 2
        cnt += 1
    tbl_file.close()
    txt_file.close()
    print "Total %d char." % cnt

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Bad argv.')
        sys.exit(0)

    if sys.argv[1] == '-r':
        batch_replace_txt(sys.argv[2], sys.argv[3])
        sys.exit(0)

    fd = os.open(sys.argv[2], os.O_RDONLY)
    size = os.fstat(fd).st_size
    #buf = mmap.mmap(fd, size, prot=mmap.PROT_READ)
    buf = mmap.mmap(fd, size, access=mmap.ACCESS_READ)
    if sys.argv[1] == '-m':
        make_tbl(buf, size, sys.argv[3])
        
    os.close(fd)
