from PyPDF2 import PdfFileReader, PdfFileMerger
from sectime import setctime
from timestamp import to_timestamp
import os


def set_pdf_metadata(path_src, path_dst):
    file = open(path_src, 'rb')
    merger = PdfFileMerger()
    merger.append(file)
    fout = open(f"{path_dst}", 'wb')
    merger.write(fout)
    file.close()
    fout.close()
    try:
        setctime(f"{path_dst}", to_timestamp("23/03/1998 12:12:48"))
    except Exception as e:
        print(e)
    os.utime(f"{path_dst}", (os.path.getctime(path_src), os.path.getmtime(path_src)))


def get_pdf_metadata(path):
    file = open(path, 'rb')
    reader = PdfFileReader(file)
    metadata = reader.getDocumentInfo()
    file.close()
    return metadata

if __name__ == '__main__':
    set_pdf_metadata("../r.pdf", "../g.pdf")

