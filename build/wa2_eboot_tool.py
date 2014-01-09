#For WHITE ALBUM2 PS3 File Script
#By KiD
#Ref: http://blog.lse.epita.fr/articles/8-static-analysis-of-an-unknown-compression-format.html


import mmap
import os
import pylzma
import struct
import sys

UNCOMP_BLOCK_SIZE = 0x10000
EBOOT_OFFSET = 0x10000
WA2_EBOOT101_INDEX = 0x10765C
LZMA_PAD = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

def compress(buf, size, out):
    remain = size
    pos = 0
    comp_size = 0
    num_blocks = 0
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
        dst = pylzma.compress(block, dictionary=14, eos=0)[5:]
        head += struct.pack("I8s", len(dst), "\x5d\x00\x40\x00\x00\x00\x00\x00")
        out.write(head+dst)
        pad = len(head+dst)
        comp_size += pad
        pad = (pad + 0xf) / 0x10 * 0x10 - pad
        if (pad > 0) :
            out.write(LZMA_PAD[0:pad])
            comp_size += pad
    print "compress %d->%d, block %d." % (size, comp_size, num_blocks)

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
    

def import_to_eboot(buf):
    print "Not yet"

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
        import_to_eboot(buf)
    elif sys.argv[1] == '-d':
        decompress(buf, 0, size, sys.argv[3], 1)
    elif sys.argv[1] == '-c':
        compress(buf, size, open(sys.argv[3], "wb+"))
    else:
        print 'Bad argv.'
    os.close(fd)
