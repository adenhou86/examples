import os
import torch
import wandb
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import Dataset, DatasetDict
from PyPDF2 import PdfReader

# 1. Directory of PDFs
PDF_DIR = "path/to/your/pdf/directory"
OUTPUT_DIR = "./mixtral_finetuned"

# 2. Function to extract text from PDFs
def pdf_to_text(file_path):
    reader = PdfReader(file_path)
    text = "".join([page.extract_text() for page in reader.pages])
    return text

# 3. Preprocess all PDFs and load text into a dataset
def load_pdf_data(pdf_dir):
    documents = []
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            file_path = os.path.join(pdf_dir, pdf_file)
            text = pdf_to_text(file_path)
            documents.append(text)
    return documents

print("Extracting text from PDFs...")
documents = load_pdf_data(PDF_DIR)

# Split documents into smaller chunks (e.g., ~500 tokens each)
print("Splitting documents into chunks...")
def split_into_chunks(text, chunk_size=500):
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

all_chunks = []
for doc in documents:
    all_chunks.extend(split_into_chunks(doc))

data_dict = {"text": all_chunks}

# Create a dataset
dataset = Dataset.from_dict(data_dict)

# Split into train and validation sets
data = dataset.train_test_split(test_size=0.1)

# 4. Load Mixtral tokenizer and model
model_name = "mixtral-8x7B"  # Replace with the actual Mixtral model name or path
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 5. Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

tokenized_data = data.map(tokenize_function, batched=True, remove_columns=["text"])

# 6. Define custom data collator
def data_collator(batch):
    return {
        'input_ids': torch.stack([torch.tensor(example['input_ids']) for example in batch]),
        'attention_mask': torch.stack([torch.tensor(example['attention_mask']) for example in batch]),
    }

# 7. Initialize wandb for tracking
wandb.init(project="mixtral-sec-filings", name="finetune-10q-run")

# 8. Define training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    weight_decay=0.01,
    logging_steps=10,
    save_steps=100,
    eval_steps=100,
    evaluation_strategy="steps",
    save_strategy="steps",
    fp16=True,
    optim="adamw_torch",
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    logging_dir="./logs",
    logging_first_step=True,
    report_to=["wandb"],
    save_total_limit=2,
)

# 9. Define Trainer class
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data["train"],
    eval_dataset=tokenized_data["test"],
    tokenizer=tokenizer,
    data_collator=data_collator
)

# 10. Train the model
print("Starting training...")
trainer.train()

# 11. Save the final model
print("Saving the model...")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("Fine-tuning complete. Model saved to", OUTPUT_DIR)
