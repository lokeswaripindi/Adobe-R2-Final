import os
import json
from utils.extractor import extract_headings_from_pdf

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def process_all_pdfs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        if not filename.lower().endswith(".pdf"):
            continue

        filepath = os.path.join(INPUT_DIR, filename)
        print(f"[📄] Processing: {filename}")

        title = filename.replace(".pdf", "")
        outline = extract_headings_from_pdf(filepath)

        output_data = {
            "title": title,
            "outline": outline
        }

        output_filename = filename.replace(".pdf", ".json")
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)

        print(f"[✅] Saved: {output_filename}")

if __name__ == "__main__":
    process_all_pdfs()
