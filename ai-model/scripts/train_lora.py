"""Дообучение (LoRA) базовой модели под наставника платформы.

Требуется Python 3.10+ и желательно GPU с 6+ ГБ VRAM.
Запуск: python scripts/train_lora.py
"""

from __future__ import annotations

import json
from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "train.jsonl"
OUTPUT_DIR = ROOT / "output" / "ai-academy-mentor"

BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
MAX_SEQ_LENGTH = 1024
EPOCHS = 3
BATCH_SIZE = 2
LEARNING_RATE = 2e-4


def load_rows() -> list[dict]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Нет {DATA_PATH}. Сначала выполните: python scripts/build_dataset.py"
        )
    rows: list[dict] = []
    for line in DATA_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def format_chat(row: dict, tokenizer) -> str:
    return tokenizer.apply_chat_template(row["messages"], tokenize=False, add_generation_prompt=False)


def main() -> None:
    rows = load_rows()
    print(f"Загружено примеров: {len(rows)}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    print(f"Устройство: {device}")

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=dtype,
        device_map="auto" if device == "cuda" else None,
        trust_remote_code=True,
    )
    if device == "cpu":
        model = model.to(device)

    lora = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    texts = [format_chat(row, tokenizer) for row in rows]
    dataset = Dataset.from_dict({"text": texts})

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=4,
        learning_rate=LEARNING_RATE,
        logging_steps=5,
        save_strategy="epoch",
        fp16=device == "cuda",
        report_to="none",
        remove_unused_columns=False,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        max_seq_length=MAX_SEQ_LENGTH,
    )
    trainer.train()
    trainer.model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"Модель сохранена в {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
