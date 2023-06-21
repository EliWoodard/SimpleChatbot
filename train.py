import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding
import pickle

# Parameters
batch_size = 64
epochs = 100
latent_dim = 256
max_len = 100
max_words = 1000
embedding_dim = 25  # You can change the size of embeddings
training_data_directory = "TrainingData"

# Load data
input_train = np.load(f"{training_data_directory}/input_train.npy")
input_test = np.load(f"{training_data_directory}/input_test.npy")
response_train = np.load(f"{training_data_directory}/response_train.npy")
response_test = np.load(f"{training_data_directory}/response_test.npy")

# Load tokenizer
with open(f"{training_data_directory}/tokenizer.pkl", "rb") as file:
    tokenizer = pickle.load(file)

# OPTIONAL: Load pre-trained embeddings like GloVe
# embeddings_index = ...
# embedding_matrix = np.zeros((max_words, embedding_dim))
# for word, i in tokenizer.word_index.items():
#     embedding_vector = embeddings_index.get(word)
#     if embedding_vector is not None:
#         embedding_matrix[i] = embedding_vector

# Seq2Seq model
# Encoder
encoder_inputs = Input(shape=(max_len,))
# If using pre-trained embeddings, set weights and trainable
encoder_embedding = Embedding(max_words, embedding_dim) # , weights=[embedding_matrix], trainable=False
encoder_lstm = LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding(encoder_inputs))
encoder_states = [state_h, state_c]

# Decoder
decoder_inputs = Input(shape=(max_len,))
# If using pre-trained embeddings, set weights and trainable
decoder_embedding = Embedding(max_words, embedding_dim) # , weights=[embedding_matrix], trainable=False
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding(decoder_inputs), initial_state=encoder_states)
decoder_dense = Dense(max_words, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Model
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.summary()

# Compile & train
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

# Convert response_train and response_test to one-hot vectors
one_hot_response_train = tf.one_hot(response_train, depth=max_words)
one_hot_response_test = tf.one_hot(response_test, depth=max_words)

# Train the model
model.fit(
    [input_train, response_train], one_hot_response_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_split=0.2
)

# Save model
model.save(f'{training_data_directory}/chatbot_model.h5')
