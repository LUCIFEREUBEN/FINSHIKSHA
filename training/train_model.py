"""
Complete Training Pipeline for FinLit AI with Real Data
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from datetime import datetime
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)
from datasets import Dataset
from sklearn.model_selection import train_test_split
from rouge_score import rouge_scorer

# Configuration
BASE_DIR = Path(__file__).parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"
LOGS_DIR = BASE_DIR / "logs"

for dir_path in [MODELS_DIR, OUTPUTS_DIR, LOGS_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)

MODEL_NAME = "google/flan-t5-small"
MAX_LENGTH = 512
BATCH_SIZE = 2
LEARNING_RATE = 3e-4
NUM_EPOCHS = 3

print("="*70)
print("🎓 FINLIT AI - TRAINING WITH REAL DATA")
print("="*70)
print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"🤖 Model: {MODEL_NAME}")
print("="*70 + "\n")

# Load dataset
print("📚 STEP 1: Loading Real Dataset...")
data_path = DATASETS_DIR / "comprehensive_financial_literacy.csv"

if not data_path.exists():
    print(f"❌ Dataset not found: {data_path}")
    sys.exit(1)

df = pd.read_csv(data_path, encoding='utf-8-sig')
print(f"✅ Loaded {len(df)} samples\n")

# Split data
print("🔄 STEP 2: Splitting Data...")
train_df, test_df = train_test_split(df, test_size=0.15, random_state=42)
print(f"Training: {len(train_df)}, Testing: {len(test_df)}\n")

train_dataset = Dataset.from_pandas(train_df[['input', 'output']].reset_index(drop=True))
test_dataset = Dataset.from_pandas(test_df[['input', 'output']].reset_index(drop=True))

# Load model
print("🤖 STEP 3: Loading Model...")
print("⏳ Downloading model (2-5 minutes)...\n")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

total_params = sum(p.numel() for p in model.parameters())
print(f"✅ Model loaded: {total_params:,} parameters\n")

# Tokenize
print("⚙️ STEP 4: Tokenizing...")

def preprocess(examples):
    inputs = examples['input']
    targets = examples['output']
    model_inputs = tokenizer(inputs, max_length=MAX_LENGTH, truncation=True, padding='max_length')
    labels = tokenizer(targets, max_length=MAX_LENGTH, truncation=True, padding='max_length')
    model_inputs['labels'] = labels['input_ids']
    return model_inputs

train_dataset = train_dataset.map(preprocess, batched=True, remove_columns=['input', 'output'])
test_dataset = test_dataset.map(preprocess, batched=True, remove_columns=['input', 'output'])
print("✅ Tokenization done\n")

# Training setup
print("🏋️ STEP 5: Training Configuration...")
print(f"Epochs: {NUM_EPOCHS}, Batch: {BATCH_SIZE}, LR: {LEARNING_RATE}")
print("Expected time: 45-90 minutes on CPU\n")

output_dir = MODELS_DIR / "finlit_model"

training_args = Seq2SeqTrainingArguments(
    output_dir=str(output_dir),
    eval_strategy="epoch",  # ✅ Changed from evaluation_strategy
    learning_rate=LEARNING_RATE,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=NUM_EPOCHS,
    weight_decay=0.01,
    save_strategy="epoch",
    save_total_limit=2,
    predict_with_generate=True,
    fp16=False,
    logging_steps=5,
    load_best_model_at_end=True,
    report_to="none",
)


data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding=True)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Train
print("🚀 STEP 6: Starting Training...\n")
print("="*70)

try:
    train_result = trainer.train()
    
    print("\n💾 Saving model...")
    trainer.save_model()
    tokenizer.save_pretrained(str(output_dir))
    print(f"✅ Model saved: {output_dir}\n")
    
    # Save metrics
    metrics_dir = OUTPUTS_DIR / "training_metrics"
    metrics_dir.mkdir(exist_ok=True)
    
    with open(metrics_dir / "training_metrics.json", 'w') as f:
        json.dump(train_result.metrics, f, indent=2)
    
except Exception as e:
    print(f"\n❌ Training failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Evaluate
print("📊 STEP 7: Evaluating...\n")
eval_results = trainer.evaluate()

print("Evaluation Results:")
print("-" * 50)
for key, value in eval_results.items():
    print(f"  {key}: {value:.4f}")
print("-" * 50 + "\n")

with open(metrics_dir / "evaluation_metrics.json", 'w') as f:
    json.dump(eval_results, f, indent=2)

# Test predictions
print("🧪 STEP 8: Testing Predictions...\n")

test_samples = test_df.sample(n=min(3, len(test_df)))

for idx, row in test_samples.iterrows():
    print(f"\n{'='*70}")
    print(f"Test Example {idx + 1}:")
    print(f"{'='*70}")
    print(f"\n❓ Question:\n{row['input']}\n")
    print(f"✅ Expected:\n{row['output'][:150]}...\n")
    
    inputs = tokenizer(row['input'], return_tensors="pt", max_length=MAX_LENGTH, truncation=True)
    outputs = model.generate(**inputs, max_length=MAX_LENGTH, num_beams=4, early_stopping=True)
    prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print(f"🤖 Predicted:\n{prediction}\n")
    print("="*70)

# Visualization
print("\n📊 STEP 9: Creating Visualization...")

try:
    history = trainer.state.log_history
    
    train_loss = [x['loss'] for x in history if 'loss' in x]
    eval_loss = [x['eval_loss'] for x in history if 'eval_loss' in x]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Loss plot
    ax1.plot(train_loss, 'b-', linewidth=2, label='Training Loss')
    if eval_loss:
        ax1.plot(np.linspace(0, len(train_loss)-1, len(eval_loss)), eval_loss, 'r-', marker='o', linewidth=2, label='Validation Loss')
    ax1.set_xlabel('Steps', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Loss', fontsize=12, fontweight='bold')
    ax1.set_title('Training Progress', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Info
    ax2.axis('off')
    info_text = f"""
    FINLIT AI - TRAINING SUMMARY
    {'='*40}
    
    Model: {MODEL_NAME}
    Total Parameters: {total_params:,}
    
    Dataset: Real Financial Literacy Data
    Training Samples: {len(train_df)}
    Testing Samples: {len(test_df)}
    
    Epochs: {NUM_EPOCHS}
    Batch Size: {BATCH_SIZE}
    Learning Rate: {LEARNING_RATE}
    
    Final Training Loss: {train_loss[-1]:.4f}
    Final Validation Loss: {eval_loss[-1] if eval_loss else 'N/A'}
    
    Status: ✅ Training Completed
    Saved: {output_dir.name}/
    """
    ax2.text(0.1, 0.5, info_text, fontsize=10, family='monospace', verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    plt.tight_layout()
    plot_path = metrics_dir / "training_visualization.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved: {plot_path}")
    plt.show()
    
except Exception as e:
    print(f"⚠️ Visualization failed: {e}")

# Final summary
print("\n" + "="*70)
print("✅ TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
print("="*70)
print(f"📅 Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"💾 Model: {output_dir}")
print(f"📊 Metrics: {metrics_dir}")
print(f"🎯 Your model is trained on {len(df)} real financial literacy examples!")
print("="*70 + "\n")

print("🎯 Next Steps:")
print("1. Check visualization: training_visualization.png")
print("2. Update backend to use trained model")
print("3. Test with frontend")
print("\n✅ Ready for demo!\n")
