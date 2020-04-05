import sys
import os
from PyPDF2 import PdfFileReader
def get_info(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
    
    #author = info.author
    #creator = info.creator
    #producer = info.producer
    #subject = info.subject
    if info is not None:
        title = unicode(info.title).encode('utf8')
    else:
        title = "Title not recoverd"
    print(path+"&&"+title)


if __name__ == '__main__':
    folder=sys.argv[1]
    print(folder)
    for r, d, f in os.walk(folder):
        for file in f:
            if '.pdf' in file:
                    get_info(folder+file)
