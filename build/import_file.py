#For WHITE ALBUM2 PS3 File Script
#By KiD

import os
import struct
import sys
import glob

def import_dar(name, dir):
	fd = open(name,"rb+")
	head = fd.read(0x10+0xb71*0x20)
	if (head[0:2] != "\xac\x0d" or head[8:10] != "\x71\x0b") :
		print "Bad dar file."
		fd.close()
		return
	for filename in glob.glob(dir + "/*.elzma"):
		num = int(os.path.basename(filename).split('.', 1)[0])
		size, zsize, offset = struct.unpack("LLQ", head[0x10+num*0x20:0x10+num*0x20+0x10])
		filesize = os.path.getsize(filename)
		file = open(filename, "rb")
		data = file.read()
		file_comp_size = len(data) - 4
		file_uncomp_size, = struct.unpack("1I", data[0:4])
		if (file_comp_size <= zsize) :
			fd.seek(offset, 0)
			fd.write(data[4:])
			buf = struct.pack("LL", file_uncomp_size, file_comp_size)
			head = head[0:0x10+num*0x20] + buf + head[0x10+num*0x20+8:]
			print "Import %d ok %d,%d -> %d,%d" % (num, size, zsize, file_uncomp_size, file_comp_size)
		else:
			print "Import %d error. %d,%d < %d,%d" % (num, size, zsize, file_uncomp_size, file_comp_size)
		file.close()
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Bad argv.')
        sys.exit(0)

    if sys.argv[1] == '-ip':
        import_pkgdds(sys.argv[2])
    elif sys.argv[1] == '-id' and len(sys.argv) > 3 :
        import_dar(sys.argv[2], sys.argv[3])
    else:
        print 'Bad argv.'
        
