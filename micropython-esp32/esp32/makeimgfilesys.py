import sys

OFFSET_BOOTLOADER = 0x1000
OFFSET_PARTITIONS = 0x8000
OFFSET_APPLICATION = 0x10000
OFFSET_FILESYSTEM  = 0x2C0000

files_in = [
    ('bootloader', OFFSET_BOOTLOADER, sys.argv[1]),
    ('partitions', OFFSET_PARTITIONS, sys.argv[2]),
    ('application', OFFSET_APPLICATION, sys.argv[3]),
    ('filesystem', OFFSET_FILESYSTEM, sys.argv[4]),
]
file_out = sys.argv[5]

cur_offset = OFFSET_BOOTLOADER
with open(file_out, 'wb') as fout:
    for name, offset, file_in in files_in:
        assert offset >= cur_offset
        fout.write(b'\xff' * (offset - cur_offset))
        cur_offset = offset
        with open(file_in, 'rb') as fin:
            data = fin.read()
            fout.write(data)
            cur_offset += len(data)
            print('%-12s% 8d' % (name, len(data))) 
    print('%-12s% 8d' % ('total', cur_offset))
