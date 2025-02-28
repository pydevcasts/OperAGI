from transformers import AutoModelForCausalLM, AutoTokenizer

# بارگذاری مدل و توکنایزر
model = AutoModelForCausalLM.from_pretrained(
    "Lansechen/deepseek-v2-lite-16b-chat-R1-Distill-batch8-numinamath",
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(
    "Lansechen/deepseek-v2-lite-16b-chat-R1-Distill-batch8-numinamath",
    trust_remote_code=True
)

# فرمت‌دهی ورودی
messages = [
    {"role": "user", "content": "where is capital of iran?"},
]
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)

# تولید پاسخ
outputs = model.generate(
    inputs,
    max_new_tokens=100,
    temperature=0.7,
    do_sample=True
)

# دیکد خروجی
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)