#For WHITE ALBUM2 PS3 File Script
#By KiD
#Ref: http://blog.lse.epita.fr/articles/8-static-analysis-of-an-unknown-compression-format.html


import mmap
import os
import pylzma
import struct
import sys
import codecs

UNCOMP_BLOCK_SIZE = 0x10000
EBOOT_OFFSET = 0x10000
WA2_EBOOT101_INDEX = 0x10765C
LZMA_PAD = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

def compress(buf, size):
    remain = size
    pos = 0
    comp_size = 0
    num_blocks = 0
    data = ""
    while remain > 0 :
        num_blocks += 1
        if remain > UNCOMP_BLOCK_SIZE :
            #print 'compress0 %d' % UNCOMP_BLOCK_SIZE
            head = struct.pack("I", UNCOMP_BLOCK_SIZE)
            block = buf[pos:pos+UNCOMP_BLOCK_SIZE]
            pos += UNCOMP_BLOCK_SIZE
            remain -= UNCOMP_BLOCK_SIZE
        else:
            #print 'compress1 %d' % remain
            head = struct.pack("I", remain)
            block = buf[pos:pos+remain]
            pos += remain
            remain -= remain
        dst = pylzma.compress(block, dictionary=23, fastBytes=273, eos=0)[5:]
        head += struct.pack("I8s", len(dst), "\x5d\x00\x40\x00\x00\x00\x00\x00")
        #out.write(head+dst)
        data += head+dst
        pad = len(head+dst)
        comp_size += pad
        pad = (pad + 0xf) / 0x10 * 0x10 - pad
        if (pad > 0) :
            #out.write(LZMA_PAD[0:pad])
            data += LZMA_PAD[0:pad]
            comp_size += pad
    data = struct.pack("I", size) + data
    print "compress %s  %d->%d, block %d." % (sys.argv[2], size, comp_size, num_blocks)
    return data

def decompress_block(params, block, size):
    block = params + block
    return (pylzma.decompress(block, size, maxlength=size))

def decompress(buf, uncomp_size, block_size, name, autoname = 0):
    if (uncomp_size == 0) :
        num_blocks = 999
    else :
        num_blocks = (uncomp_size + 0xFFFF) / UNCOMP_BLOCK_SIZE
    #print "block %d. %d" % (num_blocks, uncomp_size)
    pos = 0
    data = ""
    for i in xrange(num_blocks):
        block_uncomp_size, block_comp_size = struct.unpack("<II", buf[pos:pos+8])
        #print "block %x  %x" % (block_uncomp_size, block_comp_size)
        lzma_params = buf[pos+8:pos+13]
        data += decompress_block(lzma_params, buf[pos+0x10:pos+0x10+block_comp_size], block_uncomp_size)
        #out.write(data)
        if (autoname and i == 0 and len(data) > 16) :
            magic1, magic2,magic3, magic4 = struct.unpack("<IIII", data[0:0x10])
            if (magic1 == 0x67452301) :
                name += ".eg"
            elif (magic1 == 0xFF010102) :
                name += ".gtf"
            elif (magic1 == 0x53414E49) :
                name += ".inas"
            elif (magic1 > 0 and magic2 == 0 and magic3 == 0 and magic4 == 0) :
                name += ".pkgdds"
            else:
                #print "%x %x %x %x" % (magic1, magic2,magic3, magic4)
                name += ".unknown"
        pos += (block_comp_size + 0x1f) / 0x10 * 0x10
        #print "next block %x." % pos
        if (uncomp_size == 0 and pos >= block_size) :
     	    break;
    out = open(name, "wb+")
    out.write(data)
    print "decompress %s  %d(%d,%d)" % (name, len(data), uncomp_size, num_blocks)
    

def import_to_eboot(buf, dir):
    pos = WA2_EBOOT101_INDEX
    while True:
        name_offset, data_offset, uncomp_size, block_size = struct.unpack(">4I", buf[pos:pos+0x10])
        next_name_offset, next_data_offset = struct.unpack(">2I", buf[pos+0x10:pos+0x18])
        total_block = block_size
        if (next_data_offset > 0) :
            total_block = next_data_offset - data_offset
        if (name_offset == 0) : 
            break
        #print "%x %x, %x->%x" % (name_offset, data_offset, uncomp_size, block_size)
        cpos = name_offset-EBOOT_OFFSET
        name = struct.unpack("<1s", buf[cpos:cpos+1])[0]
        while True:
          cpos += 1
          n = struct.unpack("<1s", buf[cpos:cpos+1])[0]
          if n == "\x00" :
              break;
          name += n
        if name[-4:-3] == '_' :
        	name = name[:-4] + '.' + name[-3:]
        name = dir + "/" + name + ".elzma"
        if (os.path.isfile(name)) :
            fd = open(name, "rb")
            data = fd.read()
            file_comp_size = len(data) - 4
            file_uncomp_size, = struct.unpack("1I", data[0:4])
            if (file_comp_size <= total_block) :
                buf[pos+8:pos+0x10] = struct.pack(">2I", file_uncomp_size, file_comp_size)
                buf[data_offset-EBOOT_OFFSET:data_offset-EBOOT_OFFSET+file_comp_size] = data[4:]
                print "Import ok %d,%d->%d,%d  %s" % (uncomp_size, block_size, file_uncomp_size, file_comp_size, name)
            else:
                print "Import error. %d,%d < %d,%d  %x, %s" % (uncomp_size, block_size, file_uncomp_size, file_comp_size, pos, name)
                
            fd.close()
        pos += 0x10

def rebuild_eboot_file(buf, dir):
    pos = WA2_EBOOT101_INDEX
    cur_pos = 0
    end_pos = 0
    while True:
        name_offset, data_offset, uncomp_size, block_size = struct.unpack(">4I", buf[pos:pos+0x10])
        next_name_offset, next_data_offset = struct.unpack(">2I", buf[pos+0x10:pos+0x18])
        if (name_offset == 0) : 
            break
        total_block = block_size
        if (next_data_offset > 0) :
            total_block = next_data_offset - data_offset
        end_pos = data_offset-EBOOT_OFFSET+total_block
        #print "%x %x, %x->%x" % (name_offset, data_offset, uncomp_size, block_size)
        cpos = name_offset-EBOOT_OFFSET
        name = struct.unpack("<1s", buf[cpos:cpos+1])[0]
        while True:
          cpos += 1
          n = struct.unpack("<1s", buf[cpos:cpos+1])[0]
          if n == "\x00" :
              break;
          name += n
        if name[-4:-3] == '_' :
        	name = name[:-4] + '.' + name[-3:]
        name = dir + "/" + name + ".elzma"
        if (os.path.isfile(name)) :
            data = open(name, "rb").read()
            file_comp_size = len(data) - 4
            file_uncomp_size, = struct.unpack("1I", data[0:4])
            if cur_pos ==0 :
                cur_pos = data_offset-EBOOT_OFFSET
            buf[pos+4:pos+0x10] = struct.pack(">3I", cur_pos + EBOOT_OFFSET, file_uncomp_size, file_comp_size)
            buf[cur_pos:cur_pos+file_comp_size] = data[4:]
            print "Import ok %d,%d->%d,%d  %s,%x" % (uncomp_size, block_size, file_uncomp_size, file_comp_size, name, cur_pos)
            cur_pos += file_comp_size
        else :
            print "Not found %s. Rebuild failed." % name
            return
        pos += 0x10
    if (cur_pos > end_pos) :
        print "Check ELF failed. %x > %x" % (cur_pos, end_pos)
    else :
        print "Check ELF ok. %x <= %x" % (cur_pos, end_pos)

def patch_eboot_font(buf, num, buf2, num2, pngname):
	FONT1_POS=0xfedf0
	FONT1_SIZE=0x1524
	PATCH_FONT_POS=0x120d00
	buf[PATCH_FONT_POS:PATCH_FONT_POS+FONT1_SIZE]=buf[FONT1_POS:FONT1_POS+FONT1_SIZE]
	pos=PATCH_FONT_POS+FONT1_SIZE
	font_num=num-FONT1_SIZE/2
	font_code=0xf043
	tbl_buf=""
	while font_num > 0 : 
		if (font_code & 0xff) < 0x40 : 
			font_code+=1
			continue
		buf[pos:pos+2]=struct.pack(">H", font_code)
		tbl_buf+= "%x=\r\n" % font_code
		font_code+=1
		font_num-=1
		pos+=2
	#codecs.open("template.tbl", "wb+", encoding="utf-16").write(unicode(tbl_buf,'cp932'))
	print "Total charset %d, end %x" % (num, font_code)
	
	PATCH_FONT_SIZE_POS=0xca2a
	opcode=struct.unpack(">H", buf[PATCH_FONT_SIZE_POS:PATCH_FONT_SIZE_POS+2])[0]
	if opcode != 0xa92 :
		print "Bad elf."
		return
	buf[PATCH_FONT_SIZE_POS:PATCH_FONT_SIZE_POS+2]=struct.pack(">H", num)
	print "patch font size to %d" % (num)
	
	PATCH_FONT_ADDRESS=0xcaa4
	if buf[PATCH_FONT_ADDRESS:PATCH_FONT_ADDRESS+8] != "\x3C\x60\x00\x11\x30\x63\xED\xF0" :
		print "Bad elf."
		return
	buf[PATCH_FONT_ADDRESS:PATCH_FONT_ADDRESS+8]="\x3C\x60\x00\x13\x30\x63\x0D\x00"
	print "patch font address to %x" % (PATCH_FONT_POS)

	PATCH_FONT_SIZE_POS2=0xca12
	opcode=struct.unpack(">H", buf[PATCH_FONT_SIZE_POS2:PATCH_FONT_SIZE_POS2+2])[0]
	if opcode != 0x70 :
		print "Bad elf."
		return
	buf[PATCH_FONT_SIZE_POS2:PATCH_FONT_SIZE_POS2+2]=struct.pack(">H", num2)
	print "patch font2 size to %d" % (num2)
	
	PATCH_FONT_ADDRESS2=0xcba0
	PATCH_FONT_POS2=0x122c00
	if buf[PATCH_FONT_ADDRESS2:PATCH_FONT_ADDRESS2+8] != "\x3C\x60\x00\x11\x30\x63\x03\x15" :
		print "Bad elf."
		return
	buf[PATCH_FONT_ADDRESS2:PATCH_FONT_ADDRESS2+8]="\x3C\x60\x00\x13\x30\x63\x2c\x00"
	print "patch font2 address to %x" % (PATCH_FONT_POS2)
	buf[PATCH_FONT_POS2:PATCH_FONT_POS2+len(buf2)]=buf2

	LOAD_POS=0x64
	LOAD_NEW_SIZE=0x12B000
	opcode=struct.unpack(">I", buf[LOAD_POS:LOAD_POS+4])[0]
	if opcode != 0x120CE8 :
		print "Wrong elf load size."
		return
	buf[LOAD_POS:LOAD_POS+4]=struct.pack(">I", LOAD_NEW_SIZE)
	buf[LOAD_POS+8:LOAD_POS+12]=struct.pack(">I", LOAD_NEW_SIZE)
	print "patch load size to 0x%x" % LOAD_NEW_SIZE
	
	SECTION_POS=0x6ccc2c
	SECTION_NEW_SIZE=0xA358
	opcode=struct.unpack(">I", buf[SECTION_POS:SECTION_POS+4])[0]
	if opcode != 0x40 :
		print "Wrong elf section size."
		return
	buf[SECTION_POS:SECTION_POS+4]=struct.pack(">I", SECTION_NEW_SIZE)
	print "patch section size to 0x%x" % SECTION_NEW_SIZE

	png_data=open(pngname,"rb").read()
	png_size=len(png_data)-4
	PNG_WARNING_POS=0x660040
	PNG_WARNING_SIZE=0x2BA00
	if png_size > PNG_WARNING_SIZE :
		print "Wrong png size. %d > %d" % (png_size, PNG_WARNING_SIZE)
		return
	buf[PNG_WARNING_POS:PNG_WARNING_POS+png_size]=png_data[4:]
	print "patch wanring.png"
		
	
def extract(buf, outputdir):
    pos = WA2_EBOOT101_INDEX
    while True:
        name_offset, data_offset, uncomp_size, block_size = struct.unpack(">4I", buf[pos:pos+0x10])
        if name_offset == 0 : 
          break
        #print "%x %x, %x->%x" % (name_offset, data_offset, uncomp_size, block_size)
        cpos = name_offset-EBOOT_OFFSET
        name = struct.unpack("<1s", buf[cpos:cpos+1])[0]
        while True:
          cpos += 1
          n = struct.unpack("<1s", buf[cpos:cpos+1])[0]
          if n == "\x00" :
              break;
          name += n
        if name[-4:-3] == '_' :
        	name = name[:-4] + '.' + name[-3:]
        print "%s %d->%d" % (name, block_size, uncomp_size)
        open(outputdir + "/eboot/"+name+".elzma", "wb+").write(struct.pack("I", uncomp_size) + buf[data_offset-EBOOT_OFFSET:data_offset-EBOOT_OFFSET+block_size])
        decompress(buf[data_offset-EBOOT_OFFSET:data_offset-EBOOT_OFFSET+block_size], uncomp_size, block_size, outputdir + "/eboot/"+name)
        pos += 0x10

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Bad argv.')
        sys.exit(0)

    fd = os.open(sys.argv[2], os.O_RDONLY)
    size = os.fstat(fd).st_size
    #buf = mmap.mmap(fd, size, prot=mmap.PROT_READ)
    buf = mmap.mmap(fd, size, access=mmap.ACCESS_READ)
    if sys.argv[1] == '-e':
        extract(buf, sys.argv[3])
    elif sys.argv[1] == '-i':
        fd2 = os.open(sys.argv[2], os.O_RDWR)
        buf2 = mmap.mmap(fd2, size, access=mmap.ACCESS_WRITE)
        import_to_eboot(buf2, sys.argv[3])
        os.close(fd2)
    elif sys.argv[1] == '-rebuild':
        fd2 = os.open(sys.argv[2], os.O_RDWR)
        buf2 = mmap.mmap(fd2, size, access=mmap.ACCESS_WRITE)
        rebuild_eboot_file(buf2, sys.argv[3])
        os.close(fd2)
    elif sys.argv[1] == '-patch':
        fd2 = os.open(sys.argv[2], os.O_RDWR)
        buf2 = mmap.mmap(fd2, size, access=mmap.ACCESS_WRITE)
        patch_eboot_font(buf2, int(sys.argv[3]), open(sys.argv[4], "rb").read(), int(sys.argv[5]), sys.argv[6])
        os.close(fd2)
    elif sys.argv[1] == '-d':
        decompress(buf, 0, size, sys.argv[3], 1)
    elif sys.argv[1] == '-c':
        wp = open(sys.argv[3], "wb+")
        ret = compress(buf, size)
        wp.write(ret)
        wp.close()
    else:
        print 'Bad argv.'
    os.close(fd)
