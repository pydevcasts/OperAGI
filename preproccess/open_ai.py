import requests  # Importing the requests library to make HTTP requests
import openai  # Importing the OpenAI library for GPT
import os  # Importing os to manage environment variables

# Google API settings
API_KEY = 'AIzaSyCnP_Vsvo6xRGS2SbIbG6eG15NuXuB523Y'  # Your Google API key
CSE_ID = '057e93d3a50154aab'  # Your Custom Search Engine ID

# Set your OpenAI API key
openai.api_key = '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'  # Replace with your OpenAI API key

def google_search(query):
    """
    Function to perform a Google search using the Custom Search API.

    Args:
        query (str): The search query string.

    Returns:
        dict: The JSON response from the Google API containing search results or None if an error occurs.
    """
    try:
        # Constructing the URL for the API request
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}"
        response = requests.get(url)  # Sending the GET request to the API
        response.raise_for_status()  # Check if the request was successful (status code 200)
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        # Print the error message if there was an issue with the request
        print(f"Error in search: {e}")
        return None  # Return None if there was an error

def extract_context_from_results(results):
    """
    Function to extract context from the Google search results.
    This version improves the selection of snippets to provide more coherent context.
    """
    if results is None or 'items' not in results:
        return ""

    # Use a list to collect snippets
    snippets = []
    
    for item in results.get('items', []):
        if 'snippet' in item:
            snippets.append(item['snippet'])  # Collect snippets
            
    # Combine snippets into one coherent context
    context = " ".join(snippets)  # Join all snippets into one context
    return context
import time
import time

def get_answer(question):
    """
    Function to get an answer for a given question using the Google search and OpenAI's GPT model.

    Args:
        question (str): The question string to be answered.

    Returns:
        str: The answer extracted from the context or a message if no answer is found.
    """
    # Perform a Google search for the question
    search_results = google_search(question)
    
    # Extract context from the search results
    context = extract_context_from_results(search_results)
    
    # Check if context is empty, meaning no results were found
    if context == "":
        return "Unfortunately, no results were found for your question."
    
    # Retry logic for handling RateLimitError
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Use OpenAI's GPT to generate an answer based on the question and context
            response = openai.ChatCompletion.create(
                model="gpt2",
                messages=[
                    {"role": "user", "content": f"Based on the following information, answer the question: {context} Question: {question}"}
                ]
            )
            
            # Extract the answer from the OpenAI response
            answer = response['choices'][0]['message']['content']
            return answer.strip() if answer.strip() else "No answer found for your question."
        
        except openai.error.RateLimitError:
            # Wait before retrying the request
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    return "Unable to get an answer after several attempts due to rate limits."
# Prompt the user to enter a question
question = input("Please enter your question: ")
# Get the answer for the provided question
answer = get_answer(question)

# Print the answer
print("Answer:", answer)