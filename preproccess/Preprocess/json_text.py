import os
import json

# Function to process each line and generate a dictionary
def parse_line(line):
    parts = line.split('"')  # Split the line by double quotes
    audio_file = parts[1].strip()  # Extract the audio file path (second part)
    text = parts[3].strip()          # Extract the corresponding text (fourth part)
    return {
        'file_path': audio_file,  # Create a dictionary with the file path
        'text': text              # Add the text to the dictionary
    }

# Function to read the file and generate a list of dictionaries
def process_file(file_path):
    data_list = []  # Initialize an empty list to store the data
    with open(file_path, 'r', encoding='utf-8') as file:  # Open the specified file for reading
        for line in file:  # Iterate over each line in the file
            if line.strip():  # Check that the line is not empty
                data_list.append(parse_line(line))  # Parse the line and add the resulting dictionary to the list
    return data_list  # Return the list of dictionaries

# Path to the text file containing the data
text_file_path = '../audio/Persian_speech/transcript.txt'  # Specify the path to your text file here

# Process the file and obtain the list of dictionaries
data = process_file(text_file_path)  # Call the process_file function to read and parse the data

# Write the data to a new file
with open("transcript_fixed.txt", mode="w", encoding='utf-8') as file:  # Open the output file for writing
    for entry in data:  # Iterate over each entry in the data list
        # Convert the dictionary to a JSON string and write it to the file
        json.dump(entry, file, ensure_ascii=False)  # Write the JSON representation of the dictionary
        file.write('\n')  # Add a newline character for each dictionary to separate entries

# Display the data
for entry in data:  # Iterate over each entry in the data list
    print(entry)  # Print the entry to the console