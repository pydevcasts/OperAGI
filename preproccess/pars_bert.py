import requests  # Library for making HTTP requests
from transformers import BertTokenizer, BertForQuestionAnswering  # BERT model and tokenizer for QA tasks
import torch  # PyTorch for tensor operations

# Google API settings
API_KEY = 'AIzaSyCnP_Vsvo6xRGS2SbIbG6eG15NuXuB523Y'  # Replace with your Google API key
CSE_ID = '057e93d3a50154aab'  # Replace with your Custom Search Engine ID

# Load ParsBERT model and tokenizer
# model_name = "HooshvareLab/bert-fa-base-uncased"  # Pre-trained BERT model for Persian
# tokenizer = BertTokenizer.from_pretrained(model_name)  # Load the tokenizer
# model = BertForQuestionAnswering.from_pretrained(model_name)  # Load the QA model
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("HooshvareLab/bert-base-parsbert-uncased")
model = AutoModelForMaskedLM.from_pretrained("HooshvareLab/bert-base-parsbert-uncased")
def google_search(query):
    """
    Perform a Google search using the Custom Search API.

    Args:
        query (str): The search query.

    Returns:
        dict: JSON response from the Google API containing search results, or None if an error occurs.
    """
    try:
        # Construct the API request URL
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}"
        response = requests.get(url)  # Send the GET request
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        # Print the error if the request fails
        print(f"Search error: {e}")
        return None

def extract_context_from_results(results):
    """
    Extract context from Google search results.

    Args:
        results (dict): JSON response from the Google API.

    Returns:
        str: Combined context from search result snippets.
    """
    if results is None or 'items' not in results:
        return ""  # Return an empty string if no results are found

    # Collect snippets from search results
    snippets = [item['snippet'] for item in results.get('items', []) if 'snippet' in item]
    
    # Combine snippets into a single context string
    context = " ".join(snippets)
    return context

def get_answer(question):
    """
    Get an answer to a question using Google search and the BERT model.

    Args:
        question (str): The question to be answered.

    Returns:
        str: The extracted answer or a message if no answer is found.
    """
    # Perform a Google search to find relevant context
    search_results = google_search(question)
    
    # Extract context from the search results
    context = extract_context_from_results(search_results)
    
    # If no context is found, return an error message
    if not context:
        return "Unfortunately, no results were found for your question."
    
    # Tokenize the question and context for the BERT model
    inputs = tokenizer.encode_plus(question, context, return_tensors="pt", max_length=512, truncation=True)
    
    # Get the model's output (start and end logits for the answer)
    with torch.no_grad():  # Disable gradient calculation for inference
        outputs = model(**inputs)
    
    # Find the start and end positions of the answer
    answer_start = torch.argmax(outputs.start_logits)  # Start position of the answer
    answer_end = torch.argmax(outputs.end_logits) + 1  # End position of the answer

    # Convert token IDs back to text
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))
    
    # Return the answer if it's not empty, otherwise return a "no answer" message
    return answer if answer.strip() else "No answer found for your question."

# Prompt the user to enter a question
question = input("Please enter your question: ")

# Get the answer to the question
answer = get_answer(question)

# Print the answer
print("Answer:", answer)