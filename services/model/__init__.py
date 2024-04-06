from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
)


class Model:

    def __init__(self, model_name):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True)

    def predict(self, prompt):
        pipe = pipeline(task="text-generation", model=self.model,
                        tokenizer=self.tokenizer, max_length=200)
        result = pipe(f"<s>[INST] {prompt} [/INST]")

        return result[0]['generated_text']
