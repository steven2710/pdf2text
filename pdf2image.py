import pymupdf

PDF_PATH = "01.Base Command Manager Admin Guide.pdf"
doc = pymupdf.open(PDF_PATH)

for page_number, page in enumerate(doc, start=1):
    text = page.get_text("text")
    images = page.get_images(full=True)

    print(
        f"Page {page_number}: "
        f"text={len(text)} characters, "
        f"images={len(images)}"
    )

doc.close()
