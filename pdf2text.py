
import pymupdf
import json
from pathlib import Path

PDF_PATH = "07.MIG User Guide.pdf"
OUTPUT_PATH = "extracted/pages.json"


Path("extracted").mkdir(exist_ok=True)

doc = pymupdf.open(PDF_PATH)

pages = []

for page_number, page in enumerate(doc, start=1):
    text = page.get_text("text", sort=True)

    pages.append({
        "page": page_number,
        "text": text
    })

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False, indent=2)

doc.close()

print(f"Extracted {len(pages)} pages.")
print(f"Saved to {OUTPUT_PATH}")
