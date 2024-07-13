import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class TextInference:
    def __init__(self, model_name: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

    def generate_text(self, input_text: str, max_length: int = 500):
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids.to(
            self.device
        )
        generated_ids = self.model.generate(input_ids, max_length=max_length)
        return self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
