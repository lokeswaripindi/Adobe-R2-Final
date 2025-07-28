
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def rank_headings_by_relevance(headings_data, job_description, top_k=10):
    section_info = []
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    for doc in headings_data:
        for section in doc["outline"]:
            text = section["text"]
            page = section["page"]
            level = section["level"]
            embedding = model.encode(text, convert_to_tensor=True)
            score = float(util.pytorch_cos_sim(job_embedding, embedding)[0][0])

            section_info.append({
                "document": doc["title"] + ".pdf",
                "section_title": text,
                "page_number": page,
                "level": level,
                "score": round(score, 4)
            })

    ranked_sections = sorted(section_info, key=lambda x: x["score"], reverse=True)
    for idx, sec in enumerate(ranked_sections[:top_k]):
        sec["importance_rank"] = idx + 1

    return ranked_sections[:top_k]
