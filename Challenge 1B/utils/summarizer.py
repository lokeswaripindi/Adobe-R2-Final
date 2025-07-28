
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Load model
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def summarize_text(text, max_input_length=512, max_output_length=100):
    # Truncate if necessary
    input_ids = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=max_input_length, truncation=True)
    summary_ids = model.generate(input_ids, max_length=max_output_length, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
