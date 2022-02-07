from PyPDF2 import PdfFileReader, PdfFileWriter
from sectime import setctime
from timestamp import to_timestamp
import os


def set_pdf_metadata(path, metadata):
    file = open(path, 'rb')
    reader = PdfFileReader(file)
    writer = PdfFileWriter()
    writer.appendPagesFromReader(reader)
    writer.addMetadata(metadata)
    fout = open(f"{path}hjh", 'wb')
    writer.write(fout)
    file.close()
    fout.close()
    # try:
    #     setctime(f"{path}hjh", to_timestamp("23/03/1991 12:12:48"))
    # except:
    #     print("error")
    # os.utime(f"{path}hjh", (os.path.getctime(path), os.path.getmtime(path)))


def get_pdf_metadata(path):
    file = open(path, 'rb')
    reader = PdfFileReader(file)
    metadata = reader.getDocumentInfo()
    file.close()
    return metadata


set_pdf_metadata("../r.pdf", get_pdf_metadata("../r.pdf"))
