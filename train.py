import os
import torch
import glob
import math
import logging
import pandas as pd
from typing import Dict, List
from datetime import datetime
from pathlib import Path
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
    TrainerCallback
)
from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model
import PyPDF2

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handles PDF document processing and text extraction."""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            return ""

class DataProcessor:
    """Handles data loading and preprocessing."""
    
    def __init__(self, pdf_directory: str):
        self.pdf_directory = pdf_directory
        
    def load_and_preprocess_data(self) -> Dataset:
        """Load and preprocess SEC filing PDFs."""
        documents = []
        pdf_files = glob.glob(os.path.join(self.pdf_directory, "*.pdf"))
        
        for pdf_file in pdf_files:
            try:
                text = PDFProcessor.extract_text_from_pdf(pdf_file)
                if text.strip():  # Only include non-empty documents
                    # Basic preprocessing
                    text = self._preprocess_text(text)
                    documents.append({
                        "text": text,
                        "file_name": os.path.basename(pdf_file)
                    })
                    logger.info(f"Successfully processed {pdf_file}")
            except Exception as e:
                logger.error(f"Error processing {pdf_file}: {str(e)}")
        
        return Dataset.from_list(documents)
    
    @staticmethod
    def _preprocess_text(text: str) -> str:
        """Preprocess extracted text."""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        # Remove special characters but keep basic punctuation
        text = ''.join(char for char in text if char.isprintable())
        return text

class ModelHandler:
    """Handles model and tokenizer initialization and preparation."""
    
    def __init__(self, model_name: str = "mistralai/Mixtral-8x7B-v0.1"):
        self.model_name = model_name
        
    def prepare_model_and_tokenizer(self):
        """Initialize and prepare the model and tokenizer."""
        # Configure quantization
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=False
        )
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            padding_side="left",
            trust_remote_code=True
        )
        tokenizer.pad_token = tokenizer.eos_token
        
        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
        
        # Configure LoRA
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        # Prepare model for training
        model = prepare_model_for_kbit_training(model)
        model = get_peft_model(model, lora_config)
        
        return model, tokenizer

class MetricsCallback(TrainerCallback):
    """Callback for computing and logging additional metrics during training."""
    
    def __init__(self):
        self.training_stats = {
            'loss': [],
            'perplexity': [],
            'learning_rate': [],
            'epoch': []
        }
    
    def on_log(self, args, state, control, logs=None, **kwargs):
        """Compute metrics after each logging step."""
        if logs:
            if "loss" in logs:
                self.training_stats['loss'].append(logs["loss"])
                perplexity = math.exp(logs["loss"])
                self.training_stats['perplexity'].append(perplexity)
                logs["perplexity"] = perplexity
                
            if "learning_rate" in logs:
                self.training_stats['learning_rate'].append(logs["learning_rate"])
                
            if "epoch" in logs:
                self.training_stats['epoch'].append(logs["epoch"])
    
    def get_training_summary(self) -> Dict[str, float]:
        """Get summary statistics of training metrics."""
        return {
            'final_loss': self.training_stats['loss'][-1] if self.training_stats['loss'] else None,
            'final_perplexity': self.training_stats['perplexity'][-1] if self.training_stats['perplexity'] else None,
            'best_loss': min(self.training_stats['loss']) if self.training_stats['loss'] else None,
            'best_perplexity': min(self.training_stats['perplexity']) if self.training_stats['perplexity'] else None
        }

class Trainer10QFinetune:
    """Main trainer class for SEC 10-Q filings."""
    
    def __init__(self, 
                 pdf_directory: str,
                 output_dir: str,
                 model_name: str = "mistralai/Mixtral-8x7B-v0.1",
                 num_epochs: int = 3):
        self.pdf_directory = pdf_directory
        self.output_dir = output_dir
        self.model_name = model_name
        self.num_epochs = num_epochs
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
    def train(self):
        """Execute the complete training pipeline."""
        try:
            # Load and preprocess data
            logger.info("Loading and preprocessing data...")
            data_processor = DataProcessor(self.pdf_directory)
            dataset = data_processor.load_and_preprocess_data()
            
            # Prepare model and tokenizer
            logger.info("Preparing model and tokenizer...")
            model_handler = ModelHandler(self.model_name)
            model, tokenizer = model_handler.prepare_model_and_tokenizer()
            
            # Tokenize dataset
            logger.info("Tokenizing dataset...")
            tokenized_dataset = self._tokenize_dataset(dataset, tokenizer)
            
            # Prepare training arguments
            training_args = self._get_training_arguments()
            
            # Create data collator
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=tokenizer,
                mlm=False
            )
            
            # Create metrics callback
            metrics_callback = MetricsCallback()
            
            # Initialize trainer
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=tokenized_dataset,
                data_collator=data_collator,
                tokenizer=tokenizer,
                callbacks=[metrics_callback]
            )
            
            # Start training
            logger.info("Starting training...")
            train_result = trainer.train()
            
            # Save results
            self._save_results(trainer, metrics_callback, train_result)
            
            logger.info("Training completed successfully!")
            return train_result
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            raise
    
    def _tokenize_dataset(self, dataset: Dataset, tokenizer) -> Dataset:
        """Tokenize the dataset."""
        def tokenize_function(examples):
            return tokenizer(
                examples["text"],
                truncation=True,
                max_length=2048,
                padding=False,
                return_tensors=None
            )
        
        return dataset.map(
            tokenize_function,
            remove_columns=dataset.column_names,
            batched=True
        )
    
    def _get_training_arguments(self) -> TrainingArguments:
        """Configure training arguments."""
        return TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=self.num_epochs,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            learning_rate=2e-4,
            weight_decay=0.01,
            logging_steps=10,
            logging_first_step=True,
            save_steps=100,
            eval_steps=100,
            evaluation_strategy="steps",
            save_strategy="steps",
            save_total_limit=3,
            fp16=True,
            optim="paged_adamw_32bit",
            lr_scheduler_type="cosine",
            warmup_ratio=0.1,
            logging_dir=os.path.join(self.output_dir, "logs"),
            report_to=["tensorboard"],
            metric_for_best_model="loss",
            greater_is_better=False
        )
    
    def _save_results(self, trainer: Trainer, metrics_callback: MetricsCallback, train_result):
        """Save training results and metrics."""
        # Save model
        trainer.save_model()
        trainer.save_state()
        
        # Save metrics
        metrics = train_result.metrics
        trainer.save_metrics("train", metrics)
        
        # Save training summary
        summary = metrics_callback.get_training_summary()
        summary_df = pd.DataFrame([summary])
        summary_df.to_csv(os.path.join(self.output_dir, 'training_summary.csv'), index=False)
        
        # Log final metrics
        logger.info("\nTraining Summary:")
        for key, value in summary.items():
            logger.info(f"{key}: {value:.4f}")

def main():
    """Main execution function."""
    # Configuration
    PDF_DIR = "path/to/your/sec/filings"
    OUTPUT_DIR = f"output/mixtral_sec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    MODEL_NAME = "mistralai/Mixtral-8x7B-v0.1"
    NUM_EPOCHS = 3
    
    # Initialize and run trainer
    trainer = Trainer10QFinetune(
        pdf_directory=PDF_DIR,
        output_dir=OUTPUT_DIR,
        model_name=MODEL_NAME,
        num_epochs=NUM_EPOCHS
    )
    
    trainer.train()

if __name__ == "__main__":
    main()
