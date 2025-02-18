import os
import json
import torchaudio
from datasets import Dataset

# بارگذاری داده‌ها از فایل JSON
with open("transcript_list.json", "r", encoding='utf-8') as file:
    data = json.load(file)  # بارگذاری داده‌ها به عنوان لیست دیکشنری‌ها

for item in data:
    audio_file = item['file_path']
    if not os.path.exists(audio_file):
        print(f"File does not exist: {audio_file}")
    else:
        print(f"File exists: {audio_file}")
# تبدیل لیست دیکشنری‌ها به دیتاست
dataset = Dataset.from_list(data)

# تابعی برای بارگذاری فایل‌های صوتی
def load_audio(example):
    audio_file = example['file_path']
    # بررسی وجود فایل
    if not os.path.exists(audio_file):
        print(f"File does not exist: {audio_file}")
        example['audio'] = None  # یا می‌توانید یک مقدار پیش‌فرض قرار دهید
        return example
    
    try:
        example['audio'] = torchaudio.load(audio_file)[0]  # بارگذاری فایل صوتی
    except RuntimeError as e:
        print(f"Error loading audio file: {audio_file} - {e}")
        example['audio'] = None  # یا می‌توانید یک مقدار پیش‌فرض قرار دهید
    return example

# اضافه کردن داده‌های صوتی به دیتاست
dataset = dataset.map(load_audio)

# بررسی داده‌ها
print(dataset)
