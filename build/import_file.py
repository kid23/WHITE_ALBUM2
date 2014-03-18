# -*- coding: cp936 -*- 
#For WHITE ALBUM2 PS3 File Script
#By KiD

import os
import struct
import sys
import zipfile
import StringIO

EXE_TITLE = "WA2_PS3中文补丁"

def import_dar(name, zipdata):
	fd = open(name,"rb+")
	head = fd.read(0x10+0xb71*0x20)
	if (head[0:2] != "\xac\x0d" or head[8:10] != "\x71\x0b") :
		print "Bad dar file."
		fd.close()
		ErrorMessageBox("data.dar文件错误")

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
			data = filezip.read(entry.filename)
			file_comp_size = len(data) - 4
			file_uncomp_size, = struct.unpack("1I", data[0:4])
			fd.seek(0, 2)
			new_offset=fd.tell()
			fd.write(data[4:])
			buf = struct.pack("LLQ", file_uncomp_size, file_comp_size, new_offset)
			head = head[0:0x10+num*0x20] + buf + head[0x10+num*0x20+16:]
			print "Add %d ok %d,%d -> %d,%d,0x%0x" % (num, size, zsize, file_uncomp_size, file_comp_size, new_offset)
			#print "Import %d error. %d < %d" % (num, zsize, entry.file_size - 4)
	filezip.close()
	fd.seek(0,0)
	fd.write(head)
	fd.close()
	windll.user32.MessageBoxA(None, "补丁应用成功!", EXE_TITLE, 0)

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

def fix_savedata(dir):
    if (not os.path.isdir(dir) or not os.path.isfile(dir+"/SYS.BIN") ): 
        ErrorMessageBox("目录错误")
        
    import mmap
    fd = os.open(dir+"/SYS.BIN", os.O_RDWR)
    buf = mmap.mmap(fd, os.fstat(fd).st_size, access=mmap.ACCESS_WRITE)
    if (buf[0:8] != "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"): 
        print "Bad savedata or not decrypted. SYS.BIN"
        ErrorMessageBox("存档错误")
    for pos in range(0x269480, 0x269480 + 0x1258 * 100) :
        if buf[pos:pos+4] == "\0\0\0\2" :
            buf[pos+0x18:pos+0x58] = "\0\0\0\0" * 0x10
        pos+=0x1258
    os.close(fd)
    print 'Fix SYS.BIN.'
    
    import fnmatch
    zstr = "\0\0\0\0" * ((0x8A358 - 0x46358) / 4)
    for directory, subdirectories, files in os.walk(dir):
      for file in files:
        if fnmatch.fnmatch(file, 'SAVE???.BIN'):
            fd = os.open(os.path.join(directory, file), os.O_RDWR)
            buf = mmap.mmap(fd, os.fstat(fd).st_size, access=mmap.ACCESS_WRITE)
            if (buf[0:4] != "\0\0\0\2") :
                print "Bad savedata or not decrypted. %s" % file
                ErrorMessageBox("存档错误或未解密")
            buf[0x18:0x58] = "\0\0\0\0" * 0x10
            buf[0x46358:0x8A358] = zstr
            os.close(fd)
            print 'Fix %s.' % (file)
    windll.user32.MessageBoxA(None, "存档修正完成!", EXE_TITLE, 0)

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

def ErrorMessageBox(str="参数调用错误          "):
    print('Bad argv.')
    windll.user32.MessageBoxA(None, str, EXE_TITLE, 0)
    sys.exit(-1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        ErrorMessageBox()

    if sys.argv[1] == '-ip':
        import_pkgdds(sys.argv[2])
    elif sys.argv[1] == '-id' and len(sys.argv) > 3 :
        import_dar(sys.argv[2], StringIO.StringIO(open(sys.argv[3], "rb").read()))
    elif sys.argv[1] == '-fix':
        fix_savedata(sys.argv[2])
    else:
        if (sys.argv[1].endswith('BLJM60571WA2')) :
            fix_savedata(sys.argv[1])
        else :   
            try:
                res=GetResource(1,1)
            except Exception,e:
                res=None
            if res:
                import_dar(sys.argv[1], StringIO.StringIO(res))
            else :
                ErrorMessageBox()

