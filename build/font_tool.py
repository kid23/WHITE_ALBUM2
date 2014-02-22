#For WHITE ALBUM2 PS3 File Script
#By KiD

import mmap
import os
import struct
import sys
import codecs
from sets import Set

YINFU_UNICODE = u'\u266a' # 81f4 jap music char


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

def load_tbl2(name):
    TBL={}
    tbl_file = codecs.open(name, "r", encoding="utf-16")
    alllines = tbl_file.readlines()
    for eachline in alllines:
        if eachline[0] > u'7' :
            code = eachline[0:4]
            char = eachline[5:6]
            c = int(code, 16)
            TBL[c] = char
        else :
            code = eachline[0:2]
            char = eachline[3:4]
            c = int(code, 16)
            TBL[c] = char
    tbl_file.close()
    print "Load %d char." % len(TBL)
    return TBL

def replace_txt(txtname,TBL,MISSED):
    alltxt = open(txtname,"rb").read().split(',')
    newtxt = ""
    left = 0
    for txt in alltxt :
        nt = ""
        if txt.rfind(".tga") >= 0 or txt.rfind(".TGA") >= 0 or txt.rfind(".AMP") >= 0 or txt.rfind(".amp") >= 0 or txt.rfind(".ani") >= 0 or txt.rfind(".ANI") >= 0:
           nt = unicode(txt,'cp936').encode('cp932')
        else:
            cur = 0
            while cur < len(txt) :
                t1 = struct.unpack("<B", txt[cur:cur+1])
                if t1[0] >= 0x80 :
                    char = unicode(txt[cur:cur+2],'cp936')
                    if char == u'\u4f93' : 
                        char = YINFU_UNICODE
                    if TBL.has_key(char) :
                        nt += struct.pack(">H", TBL[char])
                    else :
                        nt += struct.pack(">H", TBL[u'\u3000'])
                        #nt += txt[cur:cur+2]
                        left += 1
                        MISSED.add(char)
                    cur += 2
                else :
                    nt += txt[cur:cur+1]
                    cur += 1
        newtxt += nt+","

    open(txtname, "wb+").write(newtxt[:-1])
    if left > 0 :
        print 'replace %s.(left %d)' % (txtname, left)
    else :
        print 'replace %s ok.' % (txtname)

def batch_replace_txt(dir,name):
    TBL=load_tbl(name)
    print u"blank=%x" % (TBL[u'\u3000'])
    if (not TBL.has_key(YINFU_UNICODE)) :
        print "Not found yinfu(81f4)"
        sys.exit(-1)
    print "yinfu=%x" % (TBL[YINFU_UNICODE])
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

def skip_char(buf, TBL):
    cur = 0
    last = 0
    while cur < len(buf) :
        t1 = struct.unpack("<B", buf[cur:cur+1])
        t2 = struct.unpack(">H", buf[cur:cur+2])
        if (t1[0] < 0x80) :
            if TBL.has_key(t1[0]) :
                return cur
            else:
                cur += 1
        elif TBL.has_key(t2[0]) :
            return cur
        else :
            cur += 2
    return cur

def trim_char(buf):
    cur = 0
    while cur < len(buf) :
        t1 = struct.unpack("<B", buf[cur:cur+1])
        if (t1[0]) :
            cur += 1
        else :
            break        
    return cur

def match_txt(buf, TBL):
    cur = 0
    strlen = 0
    str = u''
    ascii = 1
    while (cur < len(buf)) :
        c = struct.unpack("<B", buf[cur:cur+1])
        t = struct.unpack(">H", buf[cur:cur+2])
        if (c[0] < 0x80) :
            if TBL.has_key(c[0]) :
                str += TBL[c[0]]
                strlen += 1
                cur += 1
            elif c[0] == 0x0a :
                str += "{n}"
                strlen += 1
                cur += 1
            else :
                return (str,strlen,ascii)
        elif TBL.has_key(t[0]) :
            ascii = 0
            str += TBL[t[0]]
            strlen += 2
            cur += 2
        elif c[0] == 0:
            return (str,strlen,ascii)
        else :
            return (u'',0,1)
    return (str,strlen,ascii)
    
def export_eboot_txt(buf, size, name):
    TBL=load_tbl2(name)
    txt_file = codecs.open("EBOOT.ELF.TXT", "wb+", encoding="utf-16")
    BEGIN_OFFSET = 0x00100B74
    END_OFFSET = 0x3e3a90
    cur = BEGIN_OFFSET
    while cur < END_OFFSET :
        per = float(cur - BEGIN_OFFSET)/(END_OFFSET - BEGIN_OFFSET) * 100.0
        print "%.2f%%\r" % per,
        cur += skip_char(buf[cur:size], TBL)
        (str,strlen,ascii) = match_txt(buf[cur:size], TBL)
        #print str, strlen
        if str != u'' and strlen >= 4 and ascii == 0:
            line = u'%s,%d,%s\r\n\r\n' % ((hex(cur)), strlen, str)
            txt_file.write(line)
            cur += strlen
        else :
            cur += trim_char(buf[cur:size])
    txt_file.close()
    print "Export EBOOT.ELF.TXT end."

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
    elif sys.argv[1] == '-c':
        convert2unicode(buf, size, sys.argv[3])
    elif sys.argv[1] == '-e':	#-e eboot.elf file.tbl
        export_eboot_txt(buf, size, sys.argv[3])
    else :
        print 'Bad argv.'
        
    os.close(fd)
