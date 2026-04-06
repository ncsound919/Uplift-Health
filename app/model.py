import os
from typing import Literal

from transformers import pipeline
from llama_cpp import Llama


MODEL_BACKEND: Literal["transformers", "llama_cpp"] = os.getenv("MODEL_BACKEND", "transformers")  # or "llama_cpp"
MODEL_NAME = os.getenv("MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

_generator = None
_llama = None


def _get_transformers_pipeline():
    global _generator
    if _generator is None:
        # TinyLlama is a compact 1.1B Llama-family model suitable for constrained hardware.[web:17][web:18][web:19]
        _generator = pipeline(
            "text-generation",
            model=MODEL_NAME,
            device_map="auto",
        )
    return _generator


def _get_llama_cpp():
    global _llama
    if _llama is None:
        # Expect a local GGUF path for TinyLlama or another small chat model.[web:24][web:27]
        model_path = os.getenv("MODEL_PATH", "./tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
        _llama = Llama(model_path=model_path)
    return _llama


def generate_response(message: str) -> str:
    system_prompt = (
        "You are a concise, supportive health and wellness assistant. "
        "You do not give diagnoses and always recommend consulting a licensed professional for medical decisions."
    )
    prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{message}</s>\n<|assistant|>"

    if MODEL_BACKEND == "llama_cpp":
        llm = _get_llama_cpp()
        output = llm(prompt, max_tokens=256, stop=["</s>"])
        text = output["choices"][0]["text"]
        return text.strip()

    generator = _get_transformers_pipeline()
    outputs = generator(prompt, max_new_tokens=256, do_sample=True, top_p=0.9)
    full = outputs[0]["generated_text"]
    # Return everything after the prompt marker.
    return full.split("<|assistant|>", 1)[-1].strip()
