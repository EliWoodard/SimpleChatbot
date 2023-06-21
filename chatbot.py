from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask_cors import CORS
import pickle
import numpy as np
from sympy import sympify
import re

app = Flask(__name__)
CORS(app)  # This is important for handling cross-origin requests

# Make sure to provide the correct path to your model file and tokenizer pickle file
model_path = 'TrainingData/chatbot_model.h5'
tokenizer_path = 'TrainingData/tokenizer.pkl'

# Load model and tokenizer
model = load_model(model_path)
tokenizer = None

with open(tokenizer_path, 'rb') as file:
    tokenizer = pickle.load(file)

max_len = 100

# Define a regular expression pattern for detecting mathematical expressions
math_pattern = re.compile(r'^[\d\+\-\*/\(\)\.\s]*$')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json['user_input']

        # Check if the user input is a mathematical expression
        if math_pattern.match(user_input):
            try:
                # Evaluate the mathematical expression safely
                result = str(sympify(user_input))
                return jsonify({'response': result})
            except:
                return jsonify({'response': 'Invalid mathematical expression.'})
        
        sequence = tokenizer.texts_to_sequences([user_input])
        padded_sequence = pad_sequences(sequence, maxlen=max_len)
        
        # Generate random sequence for the second input
        random_sequence = np.random.randint(1, 100, (1, max_len))
        padded_random_sequence = pad_sequences(random_sequence, maxlen=max_len)

        # As the model has been trained to predict one-hot encoded arrays,
        # we need to decode this to text
        response_idx = np.argmax(model.predict([padded_sequence, padded_random_sequence]), axis=-1)
        
        # This function will help to convert indices back to text
        def indices_to_text(indices):
            index_to_word = {index: word for word, index in tokenizer.word_index.items()}
            return ' '.join([index_to_word.get(idx, '') for idx in indices])
        
        response_text = indices_to_text(response_idx[0])

        return jsonify({'response': response_text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run()
