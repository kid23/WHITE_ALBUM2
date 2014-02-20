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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Bad argv.')
        sys.exit(-1)

    if sys.argv[1] == '-ip':
        import_pkgdds(sys.argv[2])
    elif sys.argv[1] == '-id' and len(sys.argv) > 3 :
        import_dar(sys.argv[2], StringIO.StringIO(open(sys.argv[3], "rb").read()))
    else:
        try:
            res=GetResource(1,1)
        except Exception,e:
            res=None
        if res:
            import_dar(sys.argv[1], StringIO.StringIO(res))
        else :
            print 'Bad argv.'
            sys.exit(-1)

