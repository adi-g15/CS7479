from PyPDF3 import PdfFileReader, PdfFileWriter
import os

def decrypted_pdf_exists(fname):
    if os.path.isfile(fname):
        with open(fname, "rb") as file:
            pdf = PdfFileReader(file)
            return not pdf.getIsEncrypted()

    return False

def decrypt_pdf(filename, password):
    print(f"Decrypting {filename}...")
    file = open(filename, "rb")

    writer = PdfFileWriter()
    reader = PdfFileReader(file)

    # Already decryped
    if decrypted_pdf_exists(filename):
        return

    reader.decrypt(password)

    for page in reader.pages:
        writer.addPage(page)

    tmp_filename = filename + '.temp'

    # Write to decryped file
    with open(tmp_filename, "wb") as decrypted_file:
        writer.write(decrypted_file)

    file.close()
    os.remove(filename)
    os.rename(tmp_filename, filename)

def merge_pdfs(files, merged_name):
    print("Merging PDFs...", files)

    writer = PdfFileWriter()
    
    for file in files:
        reader = PdfFileReader(open(file, "rb"))
        for page in reader.pages:
            writer.addPage(page)

    with open(merged_name, "wb") as merged_file:
        writer.write(merged_file)

