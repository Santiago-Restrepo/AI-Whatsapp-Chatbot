from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
    BitsAndBytesConfig,
)
import torch 

class Model:

    def __init__(self, model_name, mock_model=False):
        self.mock_model = mock_model
        if mock_model:
            self.model = None
            self.tokenizer = None
            return
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True, )
        

        use_4bit = True
        bnb_4bit_compute_dtype = "float16"
        bnb_4bit_quant_type = "nf4"
        use_nested_quant = False

        device_map = {"": 0}


        compute_dtype = getattr(torch, bnb_4bit_compute_dtype)

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=use_4bit,
            bnb_4bit_quant_type=bnb_4bit_quant_type,
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=use_nested_quant,
        )

        if compute_dtype == torch.float16 and use_4bit:
            major, _ = torch.cuda.get_device_capability()
            if major >= 8:
                print("=" * 80)
                print("Your GPU supports bfloat16: accelerate training with bf16=True")
                print("=" * 80)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map=device_map
        )

    def predict(self, prompt, context=None):
        if self.mock_model:
            return "mock response"
        pipe = pipeline(task="text-generation", model=self.model,
                        tokenizer=self.tokenizer, max_new_tokens=100)
        response_separator = '[/INST]'
        result = pipe(f"{context} <s>[INST] {prompt} {response_separator}")

        generated_text = result[0]['generated_text']

        return self.extract_final_response(generated_text, response_separator)
    
    def extract_final_response(self, generated_text, response_separator='[/INST]'):
        segments = generated_text.split(response_separator)
        final_response = segments[-1].strip()
        segments = final_response.split('</s>')
        final_response = segments[0].strip()
        return final_response
