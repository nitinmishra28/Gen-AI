import torch
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from transformers import AutoModelForCausalLM, AutoTokenizer

class EvaluationService:
    def __init__(self):
        """Initializes the evaluation service."""
        self.perplexity_tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.perplexity_model = AutoModelForCausalLM.from_pretrained("gpt2")
        if torch.cuda.is_available():
            self.perplexity_model = self.perplexity_model.cuda()
        self.perplexity_model.eval()
        self.max_length = 1024  # Maximum sequence length for gpt2

    def calculate_bleu(self, reference_text: str, generated_text: str) -> float:
        """
        Calculates the BLEU score between a generated text and a reference.
        """
        reference_tokens = [reference_text.split()]
        generated_tokens = generated_text.split()
        smoother = SmoothingFunction().method4
        score = sentence_bleu(reference_tokens, generated_tokens, smoothing_function=smoother)
        return score

    def calculate_perplexity(self, text: str) -> float:
        """
        Calculates the perplexity of a given text to measure fluency.
        Lower is better.
        """
        # Encode the text and truncate to max_length
        inputs = self.perplexity_tokenizer(
            text,
            return_tensors="pt",
            max_length=self.max_length,
            truncation=True
        )
        input_ids = inputs.input_ids
        if torch.cuda.is_available():
            input_ids = input_ids.cuda()

        with torch.no_grad():
            outputs = self.perplexity_model(input_ids, labels=input_ids)
            loss = outputs.loss
        
        return torch.exp(loss).item()