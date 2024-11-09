# score.py
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def init():
    global tokenizer, model
    model_name = "EleutherAI/gpt-neo-1.3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
    )

def run(data):
    try:
        input_data = json.loads(data)
        prompt = input_data.get("prompt", "")
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        result = {"response": response[len(prompt):].strip()}
        return json.dumps(result)
    except Exception as e:
        error = str(e)
        return json.dumps({"error": error})
