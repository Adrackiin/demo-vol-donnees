
from sectime import setctime
from timestamp import to_timestamp
import os
# from PyPDF2 import PdfFileReader, PdfFileWriter
#
#
# def set_pdf_metadata(path_src, path_dst):
#     reader = PdfFileReader(path_dst)
#     writer = PdfFileWriter()
#     writer.appendPagesFromReader(reader)
#     writer.addMetadata(get_pdf_metadata(path_src))
#
#     file = open(path_src, 'rb')
#
#     fout = open(f"{path_dst}", 'wb')
#     writer.write(fout)
#     file.close()
#     fout.close()
#     try:
#         setctime(f"{path_dst}", to_timestamp("23/03/1998 12:12:48"))
#     except Exception as e:
#         print(e)
#     os.utime(f"{path_dst}", (os.path.getctime(path_src), os.path.getmtime(path_src)))
#
#
# def get_pdf_metadata(path):
#     file = open(path, 'rb')
#     reader = PdfFileReader(file)
#     metadata = reader.getDocumentInfo()
#     file.close()
#     return metadata

def windows(path_dst):
    setctime(f"{path_dst}", to_timestamp("23/03/1998 12:12:48"))

if __name__ == '__main__':
    windows("../j.pdf")
    # set_pdf_metadata("../r.pdf", "../j.pdf")

