import openai

def generate_answer(question, context_chunks):
    context_text = "\n\n".join([chunk.content for chunk in context_chunks])
    prompt = f"سوال: {question}\n\nپاسخ را بر اساس اطلاعات زیر بده:\n\n{context_text}"

    response = openai.chat.completions.create(
        model="gpt-4",  # یا gpt-3.5
        messages=[
            {"role": "system", "content": "تو یک ربات پاسخ‌گوی فارسی هستی."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()
