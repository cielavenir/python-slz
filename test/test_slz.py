import os
import slz
import zlib
import io

def test_slz():
    bytesio = io.BytesIO()
    with open(os.path.join(os.path.dirname(__file__), '10000SalesRecords.csv'), 'rb') as f:
        content = f.read()
        f.seek(0)
        l = len(content)
        siz = 1024
        cnt = (l+siz-1)//siz
        dfl = slz.compressobj()
        for i in range(cnt):
            bytesio.write(dfl.compress(f.read(siz)))
        bytesio.write(dfl.flush())
        # print(len(bytesio.getvalue()))
    bytesio.seek(0)
    ifl = zlib.decompressobj(-15)
    assert ifl.decompress(bytesio.read()) == content
