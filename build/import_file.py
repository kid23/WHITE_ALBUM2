# -*- coding: cp936 -*- 
#For WHITE ALBUM2 PS3 File Script
#By KiD

import os
import struct
import sys
import zipfile
import StringIO

def import_dar(name, zipdata):
	fd = open(name,"rb+")
	head = fd.read(0x10+0xb71*0x20)
	if (head[0:2] != "\xac\x0d" or head[8:10] != "\x71\x0b") :
		print "Bad dar file."
		fd.close()
		return
		
	filezip = zipfile.ZipFile(zipdata, "r")
	for entry in filezip.infolist():
		num = int(entry.filename.split('.', 1)[0])
		size, zsize, offset = struct.unpack("LLQ", head[0x10+num*0x20:0x10+num*0x20+0x10])
		if (entry.file_size - 4 <= zsize) :
			data = filezip.read(entry.filename)
			file_comp_size = len(data) - 4
			file_uncomp_size, = struct.unpack("1I", data[0:4])
			fd.seek(offset, 0)
			fd.write(data[4:])
			buf = struct.pack("LL", file_uncomp_size, file_comp_size)
			head = head[0:0x10+num*0x20] + buf + head[0x10+num*0x20+8:]
			print "Import %d ok %d,%d -> %d,%d" % (num, size, zsize, file_uncomp_size, file_comp_size)
		else:
			print "Import %d error. %d < %d" % (num, zsize, entry.file_size - 4)
	filezip.close()
	fd.seek(0,0)
	fd.write(head)
	fd.close()

def import_pkgdds(name):
	fd = open(name,"rb+")
	num = struct.unpack("I", fd.read(4))[0]
	fd.seek(0x10, 0)
	index = fd.read(num * 16)
	cnt = 0
	while cnt < num :
		offset, size = struct.unpack("LL", index[cnt*16:cnt*16+8])
		gtfname = "%s_%03d.gtf" % (name, cnt)
		if os.path.isfile(gtfname) :
			file = open(gtfname, "rb")
			data = file.read()
			if len(data) != size :
				print "Bad size. %s, %d(%d)" % (gtfname, len(data), size)
			else :
				fd.seek(offset, 0)
				fd.write(data)
				print "import %s ok" % gtfname
			file.close()
		cnt += 1
	fd.close()

def fix_savedata(dir,name):
    if (not os.path.isdir(dir) or not os.path.isfile(dir+"/SYS.BIN") ): 
        print "Bad dir."
        return
    fd = os.open(dir+"/SYS.BIN", os.O_RDWR)
    buf = mmap.mmap(fd, os.fstat(fd).st_size, access=mmap.ACCESS_WRITE)
    if (buf[0:8] != "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"): 
        print "Bad savedata or not decrypted. SYS.BIN"
        sys.exit(0)
    for pos in range(0x269480, 0x269480 + 0x1258 * 100) :
        if buf[pos:pos+4] == "\0\0\0\2" :
            buf[pos+0x18:pos+0x58] = "\0\0\0\0" * 0x10
        pos+=0x1258
    os.close(fd)

    import fnmatch
    zstr = "\0\0\0\0" * ((0x8A358 - 0x46358) / 4)
    for directory, subdirectories, files in os.walk(dir):
      for file in files:
        if fnmatch.fnmatch(file, 'SAVE???.BIN'):
            fd = os.open(os.path.join(directory, file), os.O_RDWR)
            buf = mmap.mmap(fd, os.fstat(fd).st_size, access=mmap.ACCESS_WRITE)
            if (buf[0:4] != "\0\0\0\2") :
                print "Bad savedata or not decrypted. %s" % file
                sys.exit(0)
            buf[0x18:0x58] = "\0\0\0\0" * 0x10
            buf[0x46358:0x8A358] = zstr
            os.close(fd)
            print 'Fix %s.' % (file)

from ctypes import *
import ctypes.wintypes

def GetModuleHandle(filename=None):
    h=windll.kernel32.GetModuleHandleW(filename)
    if not h:
        raise WinError()
    return h

def GetResource(typersc,idrsc,filename=None):
    if type(idrsc) is int:
        idrsc=u'#%d'%idrsc
    if type(typersc) is int:
        typersc=u'#%d'%typersc
    hmod=GetModuleHandle(filename)
    hrsc=windll.kernel32.FindResourceW(hmod,typersc,idrsc)
    if not hrsc:
        raise WinError()
    hData=windll.kernel32.LoadResource(hmod,hrsc)
    if not hData:
        raise WinError()
    size = windll.kernel32.SizeofResource(hmod, hrsc)
    try:
        ptr=windll.kernel32.LockResource(hData)
        try:
            data = ctypes.string_at(ptr, size)
        finally:
            UnlockResource = lambda x: None
            UnlockResource(hData)
    finally:
        windll.kernel32.FreeResource(hData)
    return data #windll.kernel32.LockResource(hglobal)[0]

def extract_dds3(name):
	data = open(name,"rb+").read()
	height,width = struct.unpack("II", data[0xc:0x14])
	cur = 0x80
	raw_r =""
	raw_g =""
	raw_b =""
	while cur < (height*width*2+0x80):
		l1,h1,l2,h2 = struct.unpack("BBBB", data[cur:cur+4])
		#l1 = struct.unpack("B", data[cur:cur+1])
		#h1 = struct.unpack("B", data[cur+1:cur+2])
		#l2 = struct.unpack("B", data[cur+2:cur+3])
		#h2 = struct.unpack("B", data[cur+3:cur+4])
		
		r = ((l1 & 0xf0)  | ((l2 & 0xf0)) >> 4)
		#r = (r << 4 | r >> 4) & 0xff
		g = ((l1 & 0xf) << 4) | (l2 & 0xf)
		#g = (g << 4 | g >> 4) & 0xff
		b = ((h1 & 0xf) << 4) | (h2 & 0xf)
		#b = (b << 4 | b >> 4) & 0xff
		#print r,g,b
		raw_r += struct.pack("B", r);
		raw_g += struct.pack("B", g);
		raw_b += struct.pack("B", b);
		cur += 4
	open("raw_r.bin","wb+").write(raw_r);
	open("raw_g.bin","wb+").write(raw_g);
	open("raw_b.bin","wb+").write(raw_b);

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Bad argv.')
        windll.user32.MessageBoxA(None, "参数调用错误", 'WA2_PS3中文补丁', 0)
        sys.exit(-1)

    if sys.argv[1] == '-ip':
        import_pkgdds(sys.argv[2])
    elif sys.argv[1] == '-id' and len(sys.argv) > 3 :
        import_dar(sys.argv[2], StringIO.StringIO(open(sys.argv[3], "rb").read()))
    elif sys.argv[1] == '-fix':
        fix_savedata(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == '-e3':
        extract_dds3(sys.argv[2])
    else:
        try:
            res=GetResource(1,1)
        except Exception,e:
            res=None
        if res:
            import_dar(sys.argv[1], StringIO.StringIO(res))
        else :
            print 'Bad argv.'
            windll.user32.MessageBoxA(None, "参数调用错误", 'WA2_PS3中文补丁', 0)
            sys.exit(-1)

