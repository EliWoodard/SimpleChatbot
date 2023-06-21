import re
import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

max_len = 100
max_words = 1000
test_split = 0.2
training_data_directory = "TrainingData"

# Read the dataset file
with open("dataset.txt", "r", encoding="utf-8") as file:
    content = file.read()

# Extract input and response pairs using regex
pairs = re.findall(r'{"instruction": "(.*?)", "context": "(.*?)", "response": "(.*?)", "category": "(.*?)"}', content, re.DOTALL)

# Separate inputs and responses
inputs = [pair[0] + " " + pair[1] for pair in pairs]
responses = [pair[2] for pair in pairs]

# Create the Tokenizer object
tokenizer = Tokenizer(num_words=max_words, oov_token="<oov>")

# Fit the tokenizer on the input and response data
tokenizer.fit_on_texts(inputs + responses)

# Convert input and response sequences to integer sequences
input_sequences = tokenizer.texts_to_sequences(inputs)
response_sequences = tokenizer.texts_to_sequences(responses)

# Pad the sequences to a fixed length
input_data = pad_sequences(input_sequences, maxlen=max_len, padding="post")
response_data = pad_sequences(response_sequences, maxlen=max_len, padding="post")

# Split the data into training and testing sets
input_train, input_test, response_train, response_test = train_test_split(
    input_data, response_data, test_size=test_split
)

# Save the tokenizer and processed data
os.makedirs(training_data_directory, exist_ok=True)
with open(os.path.join(training_data_directory, "tokenizer.pkl"), "wb") as file:
    pickle.dump(tokenizer, file)

np.save(os.path.join(training_data_directory, "input_train.npy"), input_train)
np.save(os.path.join(training_data_directory, "input_test.npy"), input_test)
np.save(os.path.join(training_data_directory, "response_train.npy"), response_train)
np.save(os.path.join(training_data_directory, "response_test.npy"), response_test)
