import pdfquery
from pypdf import PdfReader



#read the PDF
# pdf = pdfquery.PDFQuery('/home/olof/data/marketdata/data/ABB-2023-Q1.pdf')
# pdf.load()
pdf_file = '/home/olof/data/marketdata/data/ABB-2023-Q1.pdf'
with open(pdf_file, 'rb') as f:
    reader = PdfReader(f)
    number_of_pages = reader.get_num_pages()


# Extract text from a given PDF file
def extract_pdf_text(file_path):
    pdf_file = PdfReader(file_path)
    text_data = ''
    for pg in pdf_file.pages:
        text_data += pg.extractText()
    return text_data

pdf_text = extract_pdf_text('path_to_your_pdf.pdf')

