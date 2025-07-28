
import fitz  # PyMuPDF

def extract_headings_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    font_sizes = []

    # Pass 1: collect all font sizes to identify heading thresholds
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    font_sizes.append(span["size"])

    # Determine size thresholds
    unique_sizes = sorted(set(font_sizes), reverse=True)
    size_map = {unique_sizes[0]: "H1"}
    if len(unique_sizes) > 1:
        size_map[unique_sizes[1]] = "H2"
    if len(unique_sizes) > 2:
        size_map[unique_sizes[2]] = "H3"

    # Pass 2: extract headings
    headings = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text or len(text) < 3:
                        continue
                    font_size = span["size"]
                    level = size_map.get(font_size, None)
                    if level:
                        headings.append({
                            "level": level,
                            "text": text,
                            "page": page_num
                        })
    return headings
