import json

# Function to read data from a file and convert it into a list of dictionaries
def load_data(file_path):
    data_list = []  # Initialize an empty list to store the data
    with open(file_path, 'r', encoding='utf-8') as file:  # Open the file for reading
        for line in file:  # Iterate over each line in the file
            if line.strip():  # Check that the line is not empty
                data_list.append(json.loads(line.strip()))  # Convert each line to a dictionary and add it to the list
    return data_list  # Return the list of dictionaries

# Function to save data as a list into a file
def save_data(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:  # Open the output file for writing
        json.dump(data, file, ensure_ascii=False, indent=4)  # Save the data in JSON format with indentation for readability

# Path to the text file containing the data
text_file_path = './transcript_to_dict.txt'  # Specify the path to your text file here
output_file_path = './transcript_list.json'  # Specify the output file path for saving the JSON data

# Load data from the text file
data = load_data(text_file_path)  # Call the load_data function to read the data

# Display the loaded data
for entry in data:  # Iterate over each entry in the loaded data
    print(entry)  # Print the entry to the console

# Save the loaded data as a list in the output file
save_data(data, output_file_path)  # Call the save_data function to write the data to the JSON file

print(f"Data has been saved to {output_file_path}")  # Print a confirmation message indicating where the data has been saved