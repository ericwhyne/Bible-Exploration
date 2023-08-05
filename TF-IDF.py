import os
import string
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
# What files to process
file_paths = [
    "documents/Matthew-raw.txt",
    "documents/Mark-raw.txt",
    "documents/Luke-raw.txt",
    "documents/John-raw.txt"
]
# How many of the top results for each file to output
num_significant_words = 15
# After we look at output, there will be custom words we don't care about.
custom_words_file = "words_we_dont_care_about.txt"
with open(custom_words_file, "r") as file:
    custom_words = [line.strip() for line in file]

def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.lower() not in stop_words]
    tokens = [token for token in tokens if token not in custom_words]
    processed_text = ' '.join(tokens)
    return processed_text

documents = []
filenames = []
for filepath in file_paths:
    with open(filepath, 'r', encoding='utf-8') as file:
        document = file.read()
        documents.append(document)
        filenames.append(filepath)

preprocessed_documents = [preprocess_text(doc) for doc in documents]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(preprocessed_documents)
feature_names = vectorizer.get_feature_names()
tfidf_matrix_dense = tfidf_matrix.toarray()

for i, filename in enumerate(filenames):
    print(f"Document {filename}:")
    tfidf_scores = tfidf_matrix[i].toarray()[0]
    # Sort the indices of the TF-IDF scores in descending order
    top_indices = tfidf_scores.argsort()[::-1]
    # Select the top N significant words and their TF-IDF scores
    for j in range(num_significant_words):
        word_index = top_indices[j]
        word = feature_names[word_index]
        tfidf_score = tfidf_scores[word_index]
        if tfidf_score > 0:
            print(f"{word}: {tfidf_score:.4f}")
    print("\n")
