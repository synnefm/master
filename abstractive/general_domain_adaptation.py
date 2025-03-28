import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "NorGLM/NorGPT-3B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map='auto',
    torch_dtype=torch.bfloat16
)

text = "Tom ønsket å gå på barene med venner"
inputs = tokenizer(text, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=20)
