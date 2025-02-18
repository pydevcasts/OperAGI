import requests  # Importing the requests library to make HTTP requests
from transformers import BertTokenizer, BertForQuestionAnswering  # Importing the BERT tokenizer and model for question answering
import torch  # Importing PyTorch for tensor operations

# Google API settings
API_KEY = 'AIzaSyCnP_Vsvo6xRGS2SbIbG6eG15NuXuB523Y'  # Your Google API key
CSE_ID = '057e93d3a50154aab'  # Your Custom Search Engine ID

# Load the ParsBERT model and tokenizer
model_name = "HooshvareLab/bert-fa-base-uncased"  # Model name for Persian BERT
tokenizer = BertTokenizer.from_pretrained(model_name)  # Initializing the tokenizer
model = BertForQuestionAnswering.from_pretrained(model_name)  # Initializing the BERT model for question answering

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

def get_answer(question):
    """
    Function to get an answer for a given question using the Google search and BERT model.

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
    
    # Tokenize the input question and context for the model
    inputs = tokenizer.encode_plus(question, context, return_tensors="pt")
    
    # Generate the answer using the model
    with torch.no_grad():  # Disable gradient calculation for inference
        outputs = model(**inputs)  # Forward pass through the model

    # Extract start and end logits for the answer
    answer_start_scores = outputs.start_logits  # Start position logits
    answer_end_scores = outputs.end_logits  # End position logits

    # Get the index of the highest scoring start and end positions
    answer_start = torch.argmax(answer_start_scores)  # Index of the start of the answer
    answer_end = torch.argmax(answer_end_scores) + 1  # Index of the end of the answer

    # Extract the answer from the input tokens using the start and end indices
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))

    # Return the answer if it's not just whitespace, else return a no answer message
    return answer if answer.strip() else "No answer found for your question."

# Prompt the user to enter a question
question = input("Please enter your question: ")
# Get the answer for the provided question
answer = get_answer(question)

# Print the answer
print("Answer:", answer)