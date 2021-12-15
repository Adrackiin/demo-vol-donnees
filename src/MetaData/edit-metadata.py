import os

from PyPDF2 import PdfFileReader, PdfFileWriter

from sectime import setctime

'''
class PdfMeta(str):

    def writeToStream(writer, stream, encryption_key):
        stream.write(b_(writer))


def test(writer, infos):
    args = {}
    print(infos.items())
    for key, value in list(infos.items()):
        args[PdfMeta(key)] = createStringObject(value)
    print(args)
    obj = writer.getObject(writer._info)
    print(type(obj))
    print(" : ")
    print(obj)
    writer.getObject(writer._info).update(args)
'''

fin = open('../../test/test_metadata/good.pdf', 'rb')
reader = PdfFileReader(fin)

writer = PdfFileWriter()

writer.appendPagesFromReader(reader)
metadata = reader.getDocumentInfo()
writer.addMetadata(metadata)

writer.addMetadata({
    "/ModDate": "D:20000225143743+01'00'",
    "/CreationDate": "D:20000225143743+01'00'"
})


fout = open('2_edited.pdf', 'wb')
writer.write(fout)

fin.close()
fout.close()


os.utime("2_edited.pdf", (279990276, 279990276))
