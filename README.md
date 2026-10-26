pdf-translator/
├── technical_manual.pdf
├── extract_pdf.py
├── translate_pdf.py
├── extracted/
└── translated/

Trong đó:
- technical_manual.pdf: file gốc.
- extract_pdf.py: script trích xuất text.
- translate_pdf.py: script dịch bằng AI.
- extracted/: nội dung trích xuất.
- translated/: kết quả dịch.
3. Bước 2: Kiểm tra PDF có bao nhiêu trang và chứa text hay không
Đầu tiên, chưa cần gọi AI. Hãy xác định cấu trúc của file PDF.

Tạo file extract_pdf.py:
import pymupdfpdf_path = "technical_manual.pdf"doc = pymupdf.open(pdf_path)print("Total pages:", len(doc))for page_number, page in enumerate(doc, start=1):    text = page.get_text("text")    print(f"Page {page_number}: {len(text)} characters")doc.close()


Chạy:
python extract_pdf.py

Ví dụ kết quả:
Total pages: 100
Page 1: 1520 characters
Page 2: 2340 characters
Page 3: 0 characters
Page 4: 1860 characters

Cách đọc kết quả:
- Trang 1 có 1.520 ký tự: nhiều khả năng trang có text có thể trích xuất.
- Trang 2 có 2.340 ký tự: tương tự.
- Trang 3 có 0 ký tự: có thể là trang scan, trang chỉ có hình ảnh hoặc trang trống.
Không nên kết luận ngay rằng trang 3 là ảnh scan chỉ dựa vào số ký tự. Bạn cần kiểm tra hình ảnh và cấu trúc trang đó.
Kiểm tra hình ảnh trong PDF
Bổ sung đoạn code:
import pymupdfdoc = pymupdf.open("technical_manual.pdf")for page_number, page in enumerate(doc, start=1):    text = page.get_text("text")    images = page.get_images(full=True)    print(        f"Page {page_number}: "        f"text={len(text)} characters, "        f"images={len(images)}"    )doc.close()


Lưu ý rằng một trang có hình ảnh không nhất thiết là trang scan. Một trang có thể chứa cả text thực sự và nhiều hình ảnh.

Ngược lại, việc không phát hiện hình ảnh nhúng cũng chưa đủ để kết luận rằng trang không có nội dung đồ họa.
4. Bước 3: Trích xuất text từ toàn bộ PDF
Sau khi kiểm tra, bạn có thể trích xuất nội dung thành một file JSON.

Tại sao nên sử dụng JSON thay vì chỉ ghi ra file TXT?

Vì JSON cho phép bạn giữ lại số trang và nội dung tương ứng. Khi dịch xong, bạn có thể xác định bản dịch thuộc trang nào.

Tạo file extract_pdf.py:
import pymupdfimport jsonfrom pathlib import PathPDF_PATH = "technical_manual.pdf"OUTPUT_PATH = "extracted/pages.json"Path("extracted").mkdir(exist_ok=True)doc = pymupdf.open(PDF_PATH)pages = []for page_number, page in enumerate(doc, start=1):    text = page.get_text("text", sort=True)    pages.append({        "page": page_number,        "text": text    })with open(OUTPUT_PATH, "w", encoding="utf-8") as f:    json.dump(pages, f, ensure_ascii=False, indent=2)doc.close()print(f"Extracted {len(pages)} pages.")print(f"Saved to {OUTPUT_PATH}")


Chạy:
python extract_pdf.py

Kết quả là file:
extracted/pages.json

Ví dụ nội dung:
[
  {
    "page": 1,
    "text": "Introduction\nThis document describes..."
  },
  {
    "page": 2,
    "text": "Network Architecture\nThe system consists of..."
  }
]

Tham số sort=True giúp sắp xếp text theo thứ tự đọc gần với thứ tự từ trên xuống dưới, trái sang phải. Tuy nhiên, với PDF nhiều cột hoặc bố cục phức tạp, bạn vẫn phải kiểm tra kết quả.

Tài liệu tham khảo: PyMuPDF Text Extraction
Một hạn chế quan trọng
page.get_text("text") không giữ nguyên bố cục trực quan của trang.

Ví dụ, một bảng như sau:
Interface	IP Address	Status
ge-0/0/0	192.168.1.1	Up
ge-0/0/1	192.168.1.2	Down


có thể bị trích xuất thành một chuỗi văn bản mà các cột không còn được phân biệt rõ ràng.

Nếu PDF chứa nhiều bảng, bạn nên kiểm tra thêm:
tables = page.find_tables()for table in tables.tables:    print(table.extract())


Cách này hữu ích với các bảng mà PyMuPDF nhận dạng được, nhưng không đảm bảo phát hiện chính xác mọi bảng trong PDF.
