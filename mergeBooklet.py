from PyPDF2 import PdfFileReader, PdfFileWriter


def create_booklet(input_path, output_path):
    input_pdf = PdfFileReader(open(input_path, 'rb'))
    output_pdf = PdfFileWriter()

    # Get number of pages in input PDF
    num_pages = input_pdf.getNumPages()

    # Determine number of output pages
    num_output_pages = num_pages // 4
    if num_pages % 4 != 0:
        num_output_pages += 1

    # Determine page dimensions
    page = input_pdf.getPage(0)
    width, height = page.mediaBox.getWidth(), page.mediaBox.getHeight()

    for i in range(num_output_pages):
        # Determine page numbers for this sheet
        if i % 2 == 0:
            page1_num = num_pages - 2*i
            page2_num = 2*i + 1
            page3_num = num_pages - 2*i - 2
            page4_num = 2*i + 3
        else:
            page1_num = 2*i
            page2_num = num_pages - 2*i + 1
            page3_num = 2*i + 2
            page4_num = num_pages - 2*i - 1

        # Create output page
        output_page = output_pdf.addBlankPage(width=width, height=height)

        # Add pages to output page
        if page1_num <= num_pages:
            page1 = input_pdf.getPage(page1_num-1)
            output_page.mergePage(page1)
        if page2_num <= num_pages:
            page2 = input_pdf.getPage(page2_num-1)
            output_page.mergeTranslatedPage(page2, width, 0, True)
        if page3_num <= num_pages:
            page3 = input_pdf.getPage(page3_num-1)
            output_page.mergeTranslatedPage(page3, 0, -height, True)
        if page4_num <= num_pages:
            page4 = input_pdf.getPage(page4_num-1)
            output_page.mergeTranslatedPage(page4, width, -height, True)

    # Write output PDF to file
    with open(output_path, 'wb') as output_file:
        output_pdf.write(output_file)


create_booklet('input.pdf', 'output.pdf')
