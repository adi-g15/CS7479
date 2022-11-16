from os import unlink, rename, path
from shutil import copyfile
from PyPDF3 import PdfFileReader, PdfFileWriter

# The logic and the numbers are specific to our lecture notes (basically
# containing two slides in one pdf page)
def alag_pdf(pdf_name, out_name):
    output_is_same = False
    if pdf_name == out_name:
        print("[Warn] Input and output file names are same. Creating a temporary file.")
        output_is_same = True
        out_name = "temp.pdf"

    f = open(pdf_name, "rb")
    reader1 = PdfFileReader(f)

    copyfile(pdf_name, pdf_name+".tmp")

    reader2 = PdfFileReader(open(pdf_name+".tmp", "rb"))

    # DANGEROUS: delete the output file if already exists, I do this on my system
    if path.exists(out_name):
        unlink(out_name)

    outfile = open(out_name, "wb")

    w,h = reader1.getPage(0).mediaBox.upperRight

    out = PdfFileWriter()

    for i in range(len(reader1.pages)):
        p1 = reader1.getPage(i)
        p1.trimBox.upperRight = (w-25, h-75)
        p1.cropBox.upperRight = (w-25, h-75)
        p1.trimBox.lowerLeft = (25, h/2+80/4+5)
        p1.cropBox.lowerLeft = (25, h/2+80/4+5)
        out.addPage(p1)

        # We require a duplicate, else f.getPage(i) just gives us same object, so it
        # is modified twice, and both pages become same (try it if in doubt)
        p2 = reader2.getPage(i)
        p2.trimBox.lowerLeft = (25,80)
        p2.cropBox.lowerLeft = (25,80)
        p2.trimBox.upperRight = (w-25,h/2-80/4)
        p2.cropBox.upperRight = (w-25,h/2-80/4)
        out.addPage(p2)

    out.write(outfile)

    # Delete temporary duplicate
    unlink(pdf_name+".tmp")

    # Delete the output file if it was same as input file
    if output_is_same:
        rename(out_name, pdf_name)

