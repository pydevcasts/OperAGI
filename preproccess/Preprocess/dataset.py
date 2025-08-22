import os
import json
import torchaudio
from datasets import Dataset

# Load data from a JSON file
with open("transcript_list.json", "r", encoding='utf-8') as file:
    data = json.load(file)  # Load the data as a list of dictionaries

# Check the existence of audio files listed in the data
for item in data:
    audio_file = item['file_path']  # Get the audio file path from the dictionary
    if not os.path.exists(audio_file):  # Check if the file does not exist
        print(f"File does not exist: {audio_file}")  # Print a message if the file is missing
    else:
        print(f"File exists: {audio_file}")  # Print a message if the file exists

# Convert the list of dictionaries to a Dataset object
dataset = Dataset.from_list(data)

# Function to load audio files
def load_audio(example):
    audio_file = example['file_path']  # Get the audio file path from the example
    # Check if the audio file exists
    if not os.path.exists(audio_file):
        print(f"File does not exist: {audio_file}")  # Print a message if the file is missing
        example['audio'] = None  # Set audio to None or provide a default value
        return example  # Return the example with no audio loaded
    
    try:
        example['audio'] = torchaudio.load(audio_file)[0]  # Load the audio file using torchaudio
    except RuntimeError as e:
        print(f"Error loading audio file: {audio_file} - {e}")  # Print an error message if loading fails
        example['audio'] = None  # Set audio to None or provide a default value
    return example  # Return the example with the loaded audio

# Add audio data to the dataset using the load_audio function
dataset = dataset.map(load_audio)

# Display the dataset
print(dataset)  # Print the dataset to inspect its contents