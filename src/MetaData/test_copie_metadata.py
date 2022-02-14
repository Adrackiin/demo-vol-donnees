import os
import sys

from PyPDF2 import PdfFileReader, PdfFileWriter

from setctime import setctime

nameBad = sys.argv[1]
nameGood = sys.argv[2]
nameTemp = nameGood + 'tmp'

bad = open(nameBad, 'rb')
good = open(nameGood, 'rb')
fout = open(nameTemp, 'wb')

readerBad = PdfFileReader(bad)
readerGood = PdfFileReader(good)
writer = PdfFileWriter()

writer.appendPagesFromReader(readerGood)
metadata = readerBad.getDocumentInfo()
writer.addMetadata(metadata)

'''writer.addMetadata({
    "/ModDate": "D:20000225143743+01'00'",
    "/CreationDate": "D:20000225143743+01'00'"
})'''


writer.write(fout)

bad.close()
good.close()
fout.close()


setctime("2_edited.pdf", 1321369476)
os.utime("2_edited.pdf", (os.path.getmtime(nameBad), os.path.getctime(nameBad)))


os.remove(nameBad)
os.remove(nameGood)
os.rename(nameTemp, nameGood)