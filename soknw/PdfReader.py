import PyPDF2

pdfile = PyPDF2.PdfFileReader('soknw/books/PDFs/'+'Hindutva And Dalits 2020.pdf')
page = pdfile.getNumPages()
print (page)
