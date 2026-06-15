"""Локальный OpenAI-совместимый сервер для обученной модели.

Запуск: python scripts/serve.py
API: http://localhost:8001/v1/chat/completions
"""

from __future__ import annotations

import time
import uuid
from pathlib import Path
from typing import Any

import torch
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "output" / "ai-academy-mentor"
HOST = "127.0.0.1"
PORT = 8001
MODEL_NAME = "ai-academy-mentor"

app = FastAPI(title="AI Academy Mentor API")
tokenizer: AutoTokenizer | None = None
model: AutoModelForCausalLM | None = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = MODEL_NAME
    messages: list[ChatMessage]
    temperature: float = 0.4
    max_tokens: int = 256


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[dict[str, Any]]


def load_model() -> None:
    global tokenizer, model
    if not MODEL_DIR.exists():
        raise FileNotFoundError(
            f"Модель не найдена в {MODEL_DIR}. Сначала обучите: python scripts/train_lora.py"
        )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR,
        torch_dtype=dtype,
        device_map="auto" if device == "cuda" else None,
        trust_remote_code=True,
    )
    if device == "cpu":
        model = model.to(device)
    model.eval()
    print(f"Модель загружена ({device})")


@app.on_event("startup")
def startup() -> None:
    load_model()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
def chat_completions(body: ChatCompletionRequest) -> ChatCompletionResponse:
    assert tokenizer is not None and model is not None

    messages = [m.model_dump() for m in body.messages]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt")
    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=body.max_tokens,
            temperature=max(body.temperature, 0.01),
            do_sample=body.temperature > 0,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated = output[0][inputs["input_ids"].shape[-1] :]
    text = tokenizer.decode(generated, skip_special_tokens=True).strip()

    return ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
        created=int(time.time()),
        model=body.model,
        choices=[
            {
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }
        ],
    )


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, reload=False)
