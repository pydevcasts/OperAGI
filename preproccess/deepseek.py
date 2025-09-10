# deepseek.py
import requests  # Importing the requests library to make HTTP requests
import os  # Importing os to manage environment variables
import time  # Importing time for sleep in retry logic

# DeepSeek API settings
# Note: In production, use environment variables for API keys
# Example: API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_KEY = "sk-07d7791b80b844f9bee1ae786150b7ad"
API_URL = "https://api.deepseek.com/chat/completions"

def deepseek_chat(prompt, model="deepseek-reasoner", system_message="You are a professional assistant"):
    """
    Function to make API calls to DeepSeek's chat completion API.
    
    Args:
        prompt (str): The user's message or question.
        model (str): The model to use ('deepseek-reasoner' for R1 model or 'deepseek-chat' for V3 model).
        system_message (str): The system message that sets the assistant's behavior.
        
    Returns:
        dict: The JSON response from the DeepSeek API or None if an error occurs.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Check if the request was successful
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in API call: {e}")
        return None

def extract_answer_from_response(response):
    """
    Function to extract the answer from the DeepSeek API response.
    
    Args:
        response (dict): The JSON response from the DeepSeek API.
        
    Returns:
        str: The extracted answer or an error message if extraction fails.
    """
    if response is None:
        return "Failed to get a response from the API."
    
    try:
        return response['choices'][0]['message']['content']
    except (KeyError, IndexError) as e:
        print(f"Error extracting answer: {e}")
        return "Failed to extract answer from the response."

def get_deepseek_answer(prompt, model="deepseek-reasoner", system_message="You are a professional assistant"):
    """
    Function to get an answer from DeepSeek with retry logic for rate limiting.
    
    Args:
        prompt (str): The user's message or question.
        model (str): The model to use ('deepseek-reasoner' for R1 or 'deepseek-chat' for V3).
        system_message (str): The system message that sets the assistant's behavior.
        
    Returns:
        str: The answer from DeepSeek or an error message.
    """
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = deepseek_chat(prompt, model, system_message)
            return extract_answer_from_response(response)
        except Exception as e:
            # This could be a rate limit error or other API error
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Error occurred: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    return "Unable to get an answer after several attempts."

# Prompt the user to enter a question
if __name__ == "__main__":
    prompt = input("Please enter your question: ")
    
    # Get the answer for the provided question
    answer = get_deepseek_answer(prompt)
    
    # Print the answer
    print("Answer:", answer)