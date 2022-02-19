import os
from PyPDF2 import PdfFileReader, PdfFileWriter


def replace_file(path, bad, good):
    swap_file_name(path, f"{path}/{bad}", f"{path}/{good}")
    set_pdf_metadata(f"{path}/{good}", f"{path}/{bad}")
    os.remove(f"{path}/{good}")


def swap_file_name(path, file1, file2):
    dirs = os.listdir(path)
    tmp = f"{file1}.tmp"
    while tmp in dirs:
        tmp += ".tmp"
    os.rename(f"{file1}", tmp)
    os.rename(f"{file2}", f"{file1}")
    os.rename(tmp, f"{file2}")


def set_pdf_metadata(path_src, path_dst):
    metadata = get_pdf_metadata(path_src)
    writer = get_pdf_content(path_dst)
    writer.addMetadata(metadata)

    fout = open(f"{path_dst}", 'wb')
    writer.write(fout)
    fout.close()

    os.utime(f"{path_dst}", (os.path.getctime(path_src), os.path.getmtime(path_src)))


def get_pdf_metadata(path):
    file = open(path, 'rb')
    reader = PdfFileReader(file)
    metadata = reader.getDocumentInfo()
    file.close()
    return metadata


def get_pdf_content(path):
    reader = PdfFileReader(path)
    writer = PdfFileWriter()
    writer.appendPagesFromReader(reader)
    return writer


if __name__ == '__main__':
    replace_file("/home/belecesne/projetZZ2-gitlab/src", "j.pdf", "b.pdf")
