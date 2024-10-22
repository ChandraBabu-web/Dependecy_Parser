# -*- coding: utf-8 -*-
"""Telugu_MURIL_BERT_Model_DP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16kdmdBawEFqyEYUviM0AqCk09YJezPnT
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install transformers

import numpy as np
import pandas as pd

import os

# Commented out IPython magic to ensure Python compatibility.
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
import torchvision
from torch.utils.data import Dataset, DataLoader
import numpy as np
import math
# %matplotlib inline

! git clone https://github.com/EMBEDDIA/dep2label-transformers.git

cd dep2label-transformers/

"""**Encoding**"""

!python encode_dep2labels.py --input "/content/drive/My Drive/IIIT(LTRC)/Intrachunk-Train-Dev-CONLL/Telugu/train-ssf-telugu.txt" --output "/content/drive/My Drive/1train-ssf-encoded.tsv" --encoding "arc-standard"

!python encode_dep2labels.py --input "/content/drive/My Drive/IIIT(LTRC)/Intrachunk-Train-Dev-CONLL/Telugu/dev-ssf-telugu.txt" --output "/content/drive/My Drive/IIIT(LTRC)../dev-ssf-encoded.tsv" --encoding "arc-standard"

!python encode_dep2labels.py --input "/content/drive/My Drive/IIIT(LTRC)/Intrachunk-Test-CONLL/test-ssf-telugu.txt" --output "/content/drive/My Drive/IIIT(LTRC)/test-ssf-encoded.tsv" --encoding "arc-standard"

"""**Reading data**"""

import os
import re
import csv

def read_and_store_data(file_path):
    dep_data = []
    current_sentence = []
    ct = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            ct+=1
            line = line.strip()
            # Split the line by spaces
            elements = line.strip().split()

            # Skip empty lines
            #if not elements:
                #continue

            try:
                # Check if the line starts with '#' (indicating the start of a new sentence)
                if (line == ""):
                    if current_sentence:
                        # Append the current sentence to the dep_data list
                        dep_data.append(current_sentence)
                        current_sentence = []
                else:
                    # Extract Tamil word and POS tag and add it to the current_sentence list
                    dep_word = elements[0].strip()
                    dep_tag = elements[2].strip()
                    #print(current_sentence)
                    current_sentence.append({"word": dep_word, "dep_tag": dep_tag})
            except:
              except_d = 0
                #print(ct,end="=>")
                #print(elements)

        # Append the last sentence if any
        if current_sentence:
            dep_data.append(current_sentence)

    return dep_data

dataset = []
file_path1 = "/content/drive/My Drive/IIIT(LTRC)/train-ssf-encoded.tsv"
train_data = read_and_store_data(file_path1)

# Printing each sentence separately
for sentence in train_data:
    sent = []
    for data in sentence:
        sent.append((data['word'],data['dep_tag']))
    dataset.append(sent)

file_path9 = "/content/drive/My Drive/IIIT(LTRC)/dev-ssf-encoded.tsv"
test_data = read_and_store_data(file_path9)

testdataset = []
# Printing each sentence separately
for sentence in test_data:
    sent = []
    for data in sentence:
        sent.append((data['word'],data['dep_tag']))
    testdataset.append(sent)

file_path2 = "/content/drive/My Drive/IIIT(LTRC)/test-ssf-encoded.tsv"
predict_data = read_and_store_data(file_path2)

predictdataset = []
# Printing each sentence separately
for sentence in predict_data:
    sent = []
    for data in sentence:
        sent.append((data['word']))
    predictdataset.append(" ".join(sent))

#print(dataset[0:2])
print(testdataset[0:2])

print(dataset[0:2])

print(predictdataset[0:5])

train_data

"""Tags Count"""

ct_total = 0
count_L = {}
for sent in dataset:
    for tup in sent:
        if tup[1] not in count_L.keys():
            count_L[tup[1]] = 0
        count_L[tup[1]] += 1
        ct_total += 1

count_L

ct_total

len(dataset)

"""**Data preparation**"""

new_dataset = []
for sent in dataset:
    sentence = []
    tags = []
    for word, tag in sent:
        sentence.append(word)
        tags.append(tag)
    new_dataset.append([sentence,tags])
dataset = new_dataset

new_dataset = []
for sent in testdataset:
    sentence = []
    tags = []
    for word, tag in sent:
        sentence.append(word)
        tags.append(tag)
    new_dataset.append([sentence,tags])
newtestdataset = new_dataset

len(dataset)

def find_15_percent(number):

    result = 0.20 * number
    return result

input_number = len(dataset)
result = find_15_percent(input_number)
print(f"20% of {input_number} is: {result}")
print((input_number)-(result))

"""Data_split"""

import random
random.shuffle(dataset)
print(len(dataset))
print(dataset[1])

# print(len(dataset))
train_dataset = dataset[:1211]
dev_dataset = dataset[1211:]
#test_dataset = testdataset[1850:]
test_dataset = newtestdataset
print(len(train_dataset))
print(len(dev_dataset))
print(len(test_dataset))

dev_dataset

"""**Forming Vocab, word2idx, idx2word, tag2idx, idx2tag**"""

from tqdm import tqdm
vocab = []
tag_vocab = []
word2idx = {}
idx2word = {}
tag2idx = {}
idx2tag = {}

for sent in tqdm(dataset):
    for word in sent[0]:
        if word not in vocab:
            word2idx[word] = len(word2idx)
            idx2word[len(idx2word)] = word
            vocab.append(word)

for sent in tqdm(dataset):
    for tag in sent[1]:
        if tag not in tag_vocab:
            tag2idx[tag] = len(tag2idx)
            idx2tag[len(idx2tag)] = tag
            tag_vocab.append(tag)

print(tag_vocab)

word2idx

print(len(vocab))

print(f"Vocab size: {len(vocab)}")
print(f"word2idx size: {len(word2idx)}")
print(f"idx2word size: {len(idx2word)}")
print(f"tag2idx size: {len(tag2idx)}")
print(f"idx2tag size: {len(idx2tag)}")
print(vocab[1:10])

word2idx["X"] = len(word2idx)
idx2word[len(idx2word)] = "X"

word2idx["PAD"] = len(word2idx)
idx2word[len(idx2word)] = "PAD"

print(f"Vocab size: {len(vocab)}")
print(f"word2idx size: {len(word2idx)}")
print(f"idx2word size: {len(idx2word)}")
print(f"tag2idx size: {len(tag2idx)}")
print(f"idx2tag size: {len(idx2tag)}")

print(tag2idx.keys())

import numpy as np

def texts_to_sequences(text, word_index):
    sequence = []
    for token in text:
        if token in word_index.keys():
            sequence.append(word_index[token])
        else:
            sequence.append(word_index['X'])
    sequence = np.array(sequence)
    return torch.from_numpy(sequence)

"""Importing Tokenizer (muril - HuggingFace)"""

from transformers import BertTokenizer

# Load the BERT tokenizer
model_name = "monsoon-nlp/muril-adapted-local"
tokenizer = BertTokenizer.from_pretrained(model_name)

# Get the model's vocabulary
model_vocab = tokenizer.get_vocab()
#print(model_vocab)

"""Initializing the Embedding Layer"""

EMBEDDING_SIZE = 300
VOCABULARY_SIZE = len(model_vocab)

# embedding_weights = np.zeros((VOCABULARY_SIZE, EMBEDDING_SIZE))
embedding_weights = np.random.uniform(-0.05, 0.05, size=(VOCABULARY_SIZE, EMBEDDING_SIZE))

embedding_weights = torch.from_numpy(embedding_weights)

"""Defining the Model"""

class BiLSTMTagger(nn.Module):

    def __init__(self, embedding_dim, hidden_dim, vocab_size, tagset_size, pretrained_embeddings, dropout = 0.3):
        ''' Initialize the layers of this model.'''
        super(BiLSTMTagger, self).__init__()

        self.hidden_dim = hidden_dim

        # embedding layer that turns words into a vector of a specified size
        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.word_embeddings.weight.data.copy_(pretrained_embeddings)
        # the LSTM takes embedded word vectors (of a specified size) as inputs
        # and outputs hidden states of size hidden_dim
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, bidirectional=True)

        self.dropout = nn.Dropout(dropout)

        self.hidden2tag = nn.Linear(hidden_dim * 2, tagset_size)

        # initialize the hidden state (see code below)
        self.hidden = self.init_hidden()


    def init_hidden(self):
        ''' At the start of training, we need to initialize a hidden state;
           there will be none because the hidden state is formed based on perviously seen data.
           So, this function defines a hidden state with all zeroes and of a specified size.'''
        # The axes dimensions are (n_layers, batch_size, hidden_dim)
        return (torch.zeros(2, 1, self.hidden_dim),
                torch.zeros(2, 1, self.hidden_dim))

    def forward(self, sentence):
        ''' Define the feedforward behavior of the model.'''
        # create embedded word vectors for each word in a sentence
        embeds = self.word_embeddings(sentence)

        # get the output and hidden state by passing the lstm over our word embeddings
        # the lstm takes in our embeddings and hiddent state
        lstm_out, self.hidden = self.lstm(
            embeds.view(len(sentence), 1, -1), self.hidden)

        lstm_out = self.dropout(lstm_out)

        # get the scores for the most likely tag for a word
        tag_outputs = self.hidden2tag(lstm_out.view(len(sentence), -1))
        tag_scores = F.log_softmax(tag_outputs, dim=1)

        return tag_scores

"""Initializing the Model"""

EMBEDDING_DIM = 300
HIDDEN_DIM = 128

# instantiate our model
model = BiLSTMTagger(EMBEDDING_DIM, HIDDEN_DIM, len(model_vocab), len(tag2idx), embedding_weights)

# define our loss and optimizer
loss_function = nn.NLLLoss()
optimizer = optim.Adam(model.parameters())

tag_vocab
len(train_dataset)

"""Training Loop"""

import random
from sklearn.metrics import classification_report
from tqdm import tqdm

n_epochs = 25
batch_size = 7
accuracy = {}
accuracy_dev = {}
accuracy_test = {}
# Set device (CPU or GPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
for epoch in range(n_epochs):
    epoch_loss = 0.0
    epoch_correct = 0
    epoch_total = 0
    print(train_dataset)
    # train_dataset = np.array(train_dataset)
    random.shuffle(train_dataset)
    mini_batches = [train_dataset[k:k+batch_size] for k in range(0, len(train_dataset), batch_size)]

    # get all sentences and corresponding tags in the training data
    for mini_batch in tqdm(mini_batches, desc="Epoch %d" % (epoch+1)):
        try:
            # print(mini_batch)
            # zero the gradients
            model.zero_grad()

            # zero the hidden state of the LSTM, this detaches it from its history
            model.hidden = model.init_hidden()

            # prepare the inputs for processing by out network,
            # turn all sentences and targets into Tensors of numerical indices
            batch_sentences = [example[0] for example in mini_batch]
            batch_tags = [example[1] for example in mini_batch]
            #print(batch_sentences)
            # calculate the loss for each sentence in the batch and accumulate the total loss
            total_loss = 0.0
            total_correct = 0
            total_total = 0
            for sentence, tags in zip(batch_sentences, batch_tags):
                sentence_in = torch.tensor(tokenizer.encode(sentence, add_special_tokens=False))
                targets = texts_to_sequences(tags, tag2idx)
    #             print(sentence_in)
    #             print(targets)
                tag_scores = model(sentence_in)
                loss = loss_function(tag_scores, targets)
                total_loss += loss
                _, predicted_tags = torch.max(tag_scores, 1)
                for i, tag in enumerate(predicted_tags):
                    if tag == targets[i]:
                        total_correct += 1
                total_total += len(targets)

            # compute the mean loss for the batch
            batch_loss = total_loss / len(mini_batch)
            epoch_loss += batch_loss.item()
            batch_correct = total_correct / total_total
            epoch_correct += batch_correct
            epoch_total += 1

            # compute gradients and update parameters
            batch_loss.backward()
            optimizer.step()
        except:
            pass
    print("Epoch: %d, loss: %1.5f, accuracy: %1.5f" % (epoch+1, epoch_loss/epoch_total, epoch_correct/epoch_total))
    epoch_correct_dev = 0
    epoch_total_dev = 0
    with torch.no_grad():
        total_loss_dev = 0.0
        total_correct_dev = 0
        total_total_dev = 0
        for sentence, tags in dev_dataset:
            sentence_in_dev = torch.tensor(tokenizer.encode(sentence, add_special_tokens=False))
            targets_dev = texts_to_sequences(tags, tag2idx)
            tag_scores_dev = model(sentence_in_dev)
            loss_dev = loss_function(tag_scores_dev, targets_dev)
            total_loss_dev += loss_dev
            _, predicted_tags_dev = torch.max(tag_scores_dev, 1)
            for i, tag in enumerate(predicted_tags_dev):
                if tag == targets_dev[i]:
                    total_correct_dev += 1
            total_total_dev += len(targets_dev)

        # compute the mean loss for the batch
        batch_correct_dev = total_correct_dev / total_total_dev
        epoch_correct_dev += batch_correct_dev
        epoch_total_dev += 1


    accuracy[epoch+1] = epoch_correct/epoch_total
    accuracy_dev[epoch+1] = epoch_correct_dev/epoch_total_dev
    print("loss: %1.5f, accuracy: %1.5f, dev_accuracy: %1.5f" % (epoch_loss/epoch_total, epoch_correct/epoch_total, epoch_correct_dev/epoch_total_dev))

"""
Save"""

PATH = "/content/drive/MyDrive/IIIT(LTRC)/B/BertTokenizer_Method1_50K_savedModel.pth"
torch.save(model.state_dict(),PATH)

"""Load"""

PATH = "/content/drive/MyDrive/IIIT(LTRC)/B/BertTokenizer_Method1_50K_savedModel.pth"
model.load_state_dict(torch.load(PATH))

def predict(model, tokenizer, text):
    model.eval()
    with torch.no_grad():
        sentence_in = torch.tensor(tokenizer.encode(text, add_special_tokens=False))
        tag_scores = model(sentence_in)
        _, predicted_tags = torch.max(tag_scores, 1)


        predicted_labels = [idx2tag[tag.item()] for tag in predicted_tags]

    return predicted_labels
new_text = "అంతటితో	సుఖంగా కనేస్తుందా?"
predicted_labels = predict(model, tokenizer, new_text)
print("Predicted Labels:", predicted_labels)

epoch_correct_test = 0
epoch_total_test = 0
epoch_total = 0
model.eval()
with torch.no_grad():
    total_loss_test = 0.0
    total_correct_test = 0
    total_total_test = 0
    for sentence, tags in test_dataset:
        try:
            sentence_in_test = torch.tensor(tokenizer.encode(sentence, add_special_tokens=False))
            targets_test = texts_to_sequences(tags, tag2idx)
            tag_scores_test = model(sentence_in_test)
            loss_test = loss_function(tag_scores_test, targets_test)
            total_loss_test += loss_test
            epoch_total += 1
            _, predicted_tags_test = torch.max(tag_scores_test, 1)
            for i, tag in enumerate(predicted_tags_test):
                if tag == targets_test[i]:
                    total_correct_test += 1
            total_total_test += len(targets_test)
        except:
            pass
    batch_correct_test = total_correct_test / total_total_test
print("loss: %1.5f, test_accuracy: %1.5f" % (total_loss_test/epoch_total,total_correct_test/total_total_test ))

"""Prediction & Decoding

"""

def decode_tags(tags, idx2tag):
    return [idx2tag[tag] for tag in tags]


predicted_sentences = []
predicted_tags_list = []

epoch_correct_test = 0
epoch_total_test = 0
epoch_total = 0
model.eval()

with torch.no_grad():
    total_loss_test = 0.0
    total_correct_test = 0
    total_total_test = 0

    for sentence, tags in test_dataset:
        try:
            sentence_in_test = torch.tensor(tokenizer.encode(sentence, add_special_tokens=False))
            targets_test = texts_to_sequences(tags, tag2idx)
            tag_scores_test = model(sentence_in_test)
            loss_test = loss_function(tag_scores_test, targets_test)
            total_loss_test += loss_test
            epoch_total += 1

            _, predicted_tags_test = torch.max(tag_scores_test, 1)
            predicted_sentences.append(sentence)
            predicted_tags_list.append(predicted_tags_test.tolist())

            for i, tag in enumerate(predicted_tags_test):
                if tag == targets_test[i]:
                    total_correct_test += 1
            total_total_test += len(targets_test)
        except:
            pass

    batch_correct_test = total_correct_test / total_total_test

# Prints the predicted sentences and their corresponding tags
for sentence, predicted_tags in zip(predicted_sentences, predicted_tags_list):
    predicted_labels = decode_tags(predicted_tags, idx2tag)
    print("Sentence:", sentence)
    print("Predicted Labels:", predicted_labels)
    print()

print("loss: %1.5f, test_accuracy: %1.5f" % (total_loss_test / epoch_total, total_correct_test / total_total_test))

df_rows = []

for sentence, predicted_tags in zip(predicted_sentences, predicted_tags_list):
    predicted_labels = decode_tags(predicted_tags, idx2tag)


    row = {'Sentence': sentence, 'Predicted Labels': predicted_labels}


    df_rows.append(row)


df_predicted = pd.DataFrame(df_rows)


df_predicted

df_rows = []

for i, (sentence, predicted_tags) in enumerate(zip(predicted_sentences, predicted_tags_list)):
    predicted_labels = decode_tags(predicted_tags, idx2tag)


    min_length = min(len(sentence), len(predicted_labels))
    for j in range(min_length):
        df_rows.append({'Sentence': sentence[j], 'Predicted Labels': predicted_labels[j]})


df_flattened = pd.DataFrame(df_rows)



print("Flattened Predicted output DataFrame saved to: predicted_output_flattened.csv")

df_flattened

df = df_flattened

print(df)

conllx_lines = []
for idx, row in df.iterrows():
    conllx_line = f"{row['Sentence']}\t\t{row['Predicted Labels']}\n"
    conllx_lines.append(conllx_line)


output_conllx_file = "/content/drive/MyDrive/IIIT(LTRC)/B/7predicted_output.conllx"

with open(output_conllx_file, 'w', encoding='utf-8') as file:
    for line in conllx_lines:
        if line.startswith("-EOS-"):
            file.write(line + '\n')
        else:
            file.write(line)

!python decode_labels2dep.py \
  --input "/content/drive/MyDrive/IIIT(LTRC)/B/7predicted_output.conllx" \
  --output "/content/drive/My Drive/IIIT(LTRC)/B/7final_output_1.conllx" \
  --encoding "arc-standard"

"""LAS

Making of Gold Dependecies
"""

testdataset

flattened_data = [item for sublist in testdataset for item in sublist]

df = pd.DataFrame(flattened_data, columns=['Word', 'Label'])

print(df)

df

conllx_lines = []
for idx, row in df.iterrows():
    conllx_line = f"{row['Word']}\t\t{row['Label']}\n"
    conllx_lines.append(conllx_line)


output_conllx_file = "/content/drive/MyDrive/IIIT(LTRC)/B/encoded_output.conllx"

with open(output_conllx_file, 'w', encoding='utf-8') as file:
    for line in conllx_lines:
        if line.startswith("-EOS-"):
            file.write(line + '\n')
        else:
            file.write(line)

!python decode_labels2dep.py \
  --input "/content/drive/MyDrive/IIIT(LTRC)/B/encoded_output.conllx" \
  --output "/content/drive/My Drive/IIIT(LTRC)/B/5final_output_1.conllx" \
  --encoding "arc-standard"





"""RUn"""

file_path =  "/content/drive/My Drive/IIIT(LTRC)/B/5final_output_1.conllx"


try:
    data2 = pd.read_csv(file_path, sep='\t', header=None, comment='#', error_bad_lines=False, quoting=3, skip_blank_lines=False, keep_default_na=False)
    print(data2.head())
except pd.errors.ParserError as e:
    print(f"Error reading the file: {e}")

data2

words2 = data2[6].tolist()
labels2= data2[7].tolist()

df2 = pd.DataFrame({'words': words2, 'labels': labels2})
df2

df2 = pd.DataFrame({'words': words2, 'labels': labels2})

gold_dependencies_list = []
temp_dependency = []

for word, label in zip(df2['words'], df2['labels']):
    if label:

        word = int(word)
        temp_dependency.append((word, label))
    else:
        if temp_dependency:
            gold_dependencies_list.append(temp_dependency)
            temp_dependency = []


if temp_dependency:
    gold_dependencies_list.append(temp_dependency)

print(gold_dependencies_list)

"""**Making a list of predicted_dependencies**"""

file_path =  "/content/drive/My Drive/IIIT(LTRC)/B/7final_output_1.conllx"


try:
    data3 = pd.read_csv(file_path, sep='\t', header=None, comment='#', error_bad_lines=False, quoting=3, skip_blank_lines=False, keep_default_na=False)
    print(data3.head())
except pd.errors.ParserError as e:
    print(f"Error reading the file: {e}")

data3

words3 = data3[6].tolist()
labels3= data3[7].tolist()

df3 = pd.DataFrame({'words': words3, 'labels': labels3})
df3

df3 = pd.DataFrame({'words': words3, 'labels': labels3})
predicted_dependencies = []
temp_dependency = []

for word, label in zip(df3['words'], df3['labels']):
    if label:
        word = int(word)
        temp_dependency.append((word, label))
    else:
        if temp_dependency:
            predicted_dependencies.append(temp_dependency)
            temp_dependency = []


if temp_dependency:
    predicted_dependencies.append(temp_dependency)

print(predicted_dependencies)

len(gold_dependencies_list)

len(predicted_dependencies)

"""LAS

"""

def calculate_las(gold_dependencies_list, predicted_dependencies):
    total_words = 0
    correct_attachments = 0

    for gold_sentence, predicted_sentence in zip(gold_dependencies_list, predicted_dependencies):
        total_words += len(gold_sentence)
        correct_attachments += sum((gold == predicted) for gold, predicted in zip(gold_sentence, predicted_sentence))

    las = (correct_attachments / total_words) * 100
    return las



las_score = calculate_las(gold_dependencies_list, predicted_dependencies)
print(f"Labeled Attachment Score (LAS): {las_score:.2f}%")

"""UAS"""

def calculate_uas(gold_dependencies, predicted_dependencies):
    total_words = 0
    correct_heads = 0

    for gold_sentence, predicted_sentence in zip(gold_dependencies, predicted_dependencies):
        total_words += len(gold_sentence)
        correct_heads += sum((gold_head == predicted_head) for (gold_head, _), (predicted_head, _) in zip(gold_sentence, predicted_sentence))

    uas = (correct_heads / total_words) * 100
    return uas



uas_score = calculate_uas(gold_dependencies_list, predicted_dependencies)
print(f"Unlabeled Attachment Score (UAS): {uas_score:.2f}%")





!pwd

