import os
import json
import fitz  # PyMuPDF

from utils.extractor import extract_headings_from_pdf
from utils.ranker import rank_headings_by_relevance
from utils.summarizer import summarize_text

INPUT_DIR = "input"
OUTPUT_DIR = "output"

# 🔹 Load persona + job from config.json
with open("config.json", "r") as f:
    config = json.load(f)

persona = config["persona"]
job_description = f"A {persona} wants to {config['job_to_be_done']}"

print("[🧠] Job description:", job_description)

# 🔹 Create output folder if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 🔹 Step 1: Extract outline from all PDFs (no output JSONs here)
def process_all_pdfs():
    all_outlines = []

    for filename in os.listdir(INPUT_DIR):
        if not filename.lower().endswith(".pdf"):
            continue
        filepath = os.path.join(INPUT_DIR, filename)
        print(f"[📄] Processing: {filename}")

        title = filename.replace(".pdf", "")
        outline = extract_headings_from_pdf(filepath)

        all_outlines.append({
            "title": title,
            "outline": outline
        })

    return all_outlines

# 🔹 Step 2: Extract full page text from a PDF page
def extract_paragraph_from_page(pdf_path, page_number):
    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]
    return page.get_text()

# 🔹 Step 3: Full execution pipeline
def main():
    outlines = process_all_pdfs()
    ranked_sections = rank_headings_by_relevance(outlines, job_description)

    enriched_sections = []

    for section in ranked_sections:
        pdf_file = section["document"]
        page_number = section["page_number"]
        full_path = os.path.join(INPUT_DIR, pdf_file)

        try:
            paragraph = extract_paragraph_from_page(full_path, page_number)
            summary = summarize_text(paragraph)
        except Exception as e:
            summary = f"Error summarizing: {str(e)}"

        enriched_sections.append({
            **section,
            "refined_text": summary
        })

    final_output = {
        "persona": persona,
        "job_to_be_done": config["job_to_be_done"],
        "processing_timestamp": "2025-07-23",
        "extracted_sections": enriched_sections
    }

    with open(os.path.join(OUTPUT_DIR, "final_submission.json"), "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2)

    print("[🏁] Final submission with summaries saved to output/final_submission.json")

# 🔹 Entry point
if __name__ == "__main__":
    main()
