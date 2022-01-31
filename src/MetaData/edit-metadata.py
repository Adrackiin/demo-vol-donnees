from PyPDF2 import PdfFileReader, PdfFileWriter


def set_pdf_metadata(path, metadata):
    file = open(path, 'rb')
    reader = PdfFileReader(file)
    writer = PdfFileWriter()
    writer.appendPagesFromReader(reader)
    file.close()
    writer.addMetadata(metadata)
    fout = open(f"{path}h", 'wb')
    writer.write(fout)
    fout.close()


def get_pdf_metadata(path):
    file = open(path, 'rb')
    reader = PdfFileReader(file)
    metadata = reader.getDocumentInfo()
    file.close()
    return metadata


set_pdf_metadata("../t.pdf", get_pdf_metadata("../r.pdf"))
