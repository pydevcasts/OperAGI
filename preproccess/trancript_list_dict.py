
import json

# تابع برای خواندن داده‌ها از فایل و تبدیل به لیست دیکشنری‌ها
def load_data(file_path):
    data_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():  # بررسی اینکه خط خالی نباشد
                data_list.append(json.loads(line.strip()))  # تبدیل هر خط به دیکشنری
    return data_list

# تابع برای ذخیره داده‌ها به صورت یک لیست در یک فایل
def save_data(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)  # ذخیره به فرمت JSON

# مسیر فایل متنی
text_file_path = './transcript_to_dict.txt'  # مسیر فایل متنی خود را اینجا قرار دهید
output_file_path = './transcript_list.json'  # مسیر فایل خروجی

# بارگذاری داده‌ها
data = load_data(text_file_path)

# نمایش داده‌ها
for entry in data:
    print(entry)

# ذخیره داده‌ها به صورت یک لیست در فایل
save_data(data, output_file_path)

print(f"Data has been saved to {output_file_path}")