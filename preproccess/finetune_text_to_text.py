from datasets import load_dataset
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding

# Load the dataset
# ds = load_dataset("mteb/tatoeba-bitext-mining", "default")


ds = load_dataset("CohereForAI/aya_collection", "aya_dataset")

# Print the dataset structure
print(ds)

# Load the tokenizer and model
model_name = "HooshvareLab/bert-fa-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)

# Here, we'll assume we have a binary classification task
num_labels = 2  # Adjust this based on your task

model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

# Tokenization function
def tokenize_function(examples):
    return tokenizer(examples['inputs'], examples['targets'], truncation=True, padding=True)

# Tokenize the dataset
tokenized_ds = ds.map(tokenize_function, batched=True)

# Create training and test datasets
train_dataset = tokenized_ds['train']  # Use the training dataset
# If there is a validation or test dataset, you can set it up similarly
# test_dataset = tokenized_ds['test']  # Uncomment if you have a test dataset

# Define a data collator
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Create a Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=None,  # Set to your validation dataset if available
    data_collator=data_collator,
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained('./fine_tuned_model')
tokenizer.save_pretrained('./fine_tuned_model')