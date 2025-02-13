import subprocess

# اجرای دستور lsof برای یافتن پردازه‌های مرتبط با پورت 5432
command = "sudo lsof -i :80"
result = subprocess.run(
    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)

if result.returncode == 0:
    # پردازه‌های مرتبط با پورت 5432 یافت شده‌اند
    # جداگانه هر خط را بررسی کرده و پیدا کرده شده‌ی PID را ببندیم
    lines = result.stdout.split("\n")
    for line in lines:
        if "LISTEN" in line:
            pid = line.split()[1]
            # بستن پردازه با دستور kill
            kill_command = f"sudo kill {pid}"
            subprocess.run(kill_command, shell=True)
        else:
            print("پورت 80 در حال استفاده نیست.")
else:
    print("هیچ پردازه‌ای برای پورت 80 یافت نشد یا دسترسی لازم نیست.")


# deepseek.py

# import requests

# # Enter your API Key
# API_KEY = "sk-da4b4f7a4c4d41a7bd0b94f8f5566d71"  

# url = "https://api.deepseek.com/chat/completions"
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {API_KEY}"
# }

# data = {
#     "model": "deepseek-chat",  # Use 'deepseek-reasoner' for R1 model or 'deepseek-chat' for V3 model
#     "messages": [
#         {"role": "system", "content": "You are a professional assistant"},
#         {"role": "user", "content": "Who are you?"}
#     ],
#     "stream": False  # Disable streaming
# }

# data["stream"] = True

# response = requests.post(url, headers=headers, json=data, stream=True)

# for line in response.iter_lines():
#     if line:
#         decoded_line = line.decode('utf-8')
#         print(decoded_line)