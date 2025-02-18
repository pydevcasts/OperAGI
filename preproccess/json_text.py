import os
import json

# تابع برای پردازش هر خط و تولید دیکشنری
def parse_line(line):
    parts = line.split('"')
    audio_file = parts[1].strip()  # مسیر فایل صوتی
    text = parts[3].strip()          # متن مربوط به فایل صوتی
    return {
        'file_path': audio_file,
        'text': text
    }

# تابع برای خواندن فایل و تولید لیست دیکشنری‌ها
def process_file(file_path):
    data_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():  # بررسی اینکه خط خالی نباشد
                data_list.append(parse_line(line))
    return data_list

# مسیر فایل متنی
text_file_path = '../audio/Persian_speech/transcript.txt'  # مسیر فایل متنی خود را اینجا قرار دهید

# پردازش فایل و دریافت لیست دیکشنری‌ها
data = process_file(text_file_path)

# نوشتن داده‌ها به فایل
with open("transcript_fixed.txt", mode="w", encoding='utf-8') as file:
    for entry in data:
        # تبدیل دیکشنری به رشته JSON و نوشتن در فایل
        json.dump(entry, file, ensure_ascii=False)
        file.write('\n')  # اضافه کردن یک خط جدید برای هر دیکشنری

# نمایش داده‌ها
for entry in data:
    print(entry)