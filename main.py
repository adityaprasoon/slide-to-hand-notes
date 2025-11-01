from pypdf import PdfReader, PdfWriter, PageObject, PaperSize
from pypdf.annotations import FreeText
import sys

filepath = ""
if len(sys.argv) > 1:
    # We expect at least one argument after the script name
    user_string = sys.argv[1]
    filepath = user_string
else:
    # If no argument is provided, print a usage message
    print("Usage: python3 main.py \"your string argument\"")
    print("Please provide a string argument when running the script.")

pdf = PdfReader(filepath)
print(f"Page count = {len(pdf.pages)}")
oddWriter = PdfWriter()
evenWriter = PdfWriter()
margin = 10

for page_num in range(len(pdf.pages)):
    page = pdf.pages[page_num]
    newPage = PageObject.create_blank_page(width=PaperSize.A4.width, height=PaperSize.A4.height)
    page.scale_to(width=PaperSize.A4.width - margin, height=PaperSize.A4.height/2 - margin)
    newPage.merge_translated_page(page, tx=0, ty= PaperSize.A4.height/2,expand=True)

    annotation = FreeText(
        text=page_num,
        rect=(50, 100, 200, 300),
        font="Arial",
        bold=True,
        font_size="14pt",
    )
    annotation.flags = 4
    if page_num % 2 == 0:
        oddWriter.add_page(newPage)
        addedToPage = oddWriter.get_num_pages()
        oddWriter.add_annotation(page_number=addedToPage - 1, annotation=annotation)
    else:
        evenWriter.add_page(newPage)
        addedToPage = evenWriter.get_num_pages()
        evenWriter.add_annotation(page_number=addedToPage -1 , annotation=annotation)

file_path_segments = filepath.split("/");
original_file_name = file_path_segments[-1].split(".")[0];
print(original_file_name)

file_path_segment_string ="/".join(file_path_segments[0:-1])

odd_file_path = f"{file_path_segment_string}/{original_file_name}-print-odd.pdf"
even_file_path = f"{file_path_segment_string}/{original_file_name}-print-even.pdf"


with open(odd_file_path, "wb") as fp:
    oddWriter.write(fp)
with open(even_file_path, "wb") as fp:
    evenWriter.write(fp)
print("Odd and even pages saved.")