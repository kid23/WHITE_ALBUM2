#For WHITE ALBUM2 PS3 File Script
#By KiD

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
    while remain > 0 :
        if remain > UNCOMP_BLOCK_SIZE :
            print 'compress0 %d' % UNCOMP_BLOCK_SIZE
            head = struct.pack("I", UNCOMP_BLOCK_SIZE)
            block = buf[pos:pos+UNCOMP_BLOCK_SIZE]
            pos += UNCOMP_BLOCK_SIZE
            remain -= UNCOMP_BLOCK_SIZE
        else:
            print 'compress1 %d' % remain
            head = struct.pack("I", remain)
            block = buf[pos:pos+remain]
            pos += remain
            remain -= remain
        dst = pylzma.compress(block, dictionary=14, eos=0)[5:]
        head += struct.pack("I8s", len(dst), "\x5d\x00\x40\x00\x00\x00\x00\x00")
    out.write(head+dst)
    pad = len(head+dst)+0xf
    pad = pad / 0x10*0x10 - pad
    if (pad > 0) :
        out.write(LZMA_PAD[0:pad])
    print "write pad %d." % pad           

def decompress_block(params, block, out, size):
    block = params + block
    out.write(pylzma.decompress(block, size, maxlength=size))

def decompress(buf, uncomp_size, block_size, out):
    num_blocks = (uncomp_size + 0xFFFF) / UNCOMP_BLOCK_SIZE
    print "block %d. %d" % (num_blocks, uncomp_size)
    pos = 0
    for i in xrange(num_blocks):
        block_uncomp_size, block_comp_size = struct.unpack("<II", buf[pos:pos+8])
        print "block %x  %x" % (block_uncomp_size, block_comp_size)
        lzma_params = buf[pos+8:pos+13]
        decompress_block(lzma_params, buf[pos+0x10:pos+0x10+block_comp_size], out, block_uncomp_size)
        pos += (block_comp_size + 0x1f) / 0x10 * 0x10
     	#print "next block %x." % pos

def extract(buf):
    pos = WA2_EBOOT101_INDEX
    while True:
        name_offset, data_offset, uncomp_size, block_size = struct.unpack(">4I", buf[pos:pos+0x10])
        if name_offset == 0 : 
          break
        print "%x %x, %x->%x" % (name_offset, data_offset, uncomp_size, block_size)
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
        decompress(buf[data_offset-EBOOT_OFFSET:data_offset-EBOOT_OFFSET+block_size], uncomp_size, block_size, open("eboot/"+name, "w"))
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
        extract(buf)
    elif sys.argv[1] == '-i':
        compress(buf, size, open("dump", "wb+"))
    elif sys.argv[1] == '-d':
        decompress(buf, 0, size, open("dump", "wb+"))
    else:
        print 'Bad argv.'
    os.close(fd)
