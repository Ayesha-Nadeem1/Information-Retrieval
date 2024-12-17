# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 23:42:58 2024

@author: Ayesha Nadeem
"""

import os
import math
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# Preprocess the text
def preprocess(document):
    words = word_tokenize(document)
    tagged_words = nltk.pos_tag(words)
    processed_doc = []
    for word, pos in tagged_words:
        if pos in ['NN', 'NNS', 'NNP', 'NNPS'] and word.lower() not in stop_words:
            processed_doc.append(word.lower())
    return processed_doc

# Create inverted index with TF-IDF scores
def create_index(dir_path):
    inverted_index = defaultdict(list)
    doc_count = defaultdict(int)
    total_docs = 0

    for filename in os.listdir(dir_path):
        if filename.endswith('.txt'):
            total_docs += 1
            with open(os.path.join(dir_path, filename), 'r', encoding='utf8') as file:
                document = file.read().lower()
                processed_doc = preprocess(document)
                doc_word_count = defaultdict(int)
                
                # Count the occurrences of each word
                for word in processed_doc:
                    doc_word_count[word] += 1
                
                # Total number of words in the document
                total_terms = len(processed_doc)
                
                # Add the words to the inverted index with normalized TF
                for word, count in doc_word_count.items():
                    tf = count / total_terms  # Normalized Term Frequency
                    inverted_index[word].append((filename, tf))
                    doc_count[word] += 1

    # Now calculate the TF-IDF score for each word
    for word in inverted_index:
        df = doc_count[word]
        idf = math.log((total_docs + 1) / (df + 1)) + 1  # Corrected IDF calculation
        for i, (doc, tf) in enumerate(inverted_index[word]):
            tfidf = tf * idf
            inverted_index[word][i] = (doc, tfidf)
    
    return inverted_index


# TF-IDF scoring function
def tf_idf(query, document, inverted_index):
    score = 0
    query_words = preprocess(query)
    for word in query_words:
        if word in inverted_index:
            for doc, tfidf in inverted_index[word]:
                if doc == document:
                    score += tfidf
    return score

# Cosine similarity calculation
def cosine_similarity(query, document, inverted_index):
    query_words = preprocess(query)
    query_vector = defaultdict(float)
    document_vector = defaultdict(float)

    for word in query_words:
        query_vector[word] += 1  # Term frequency in the query

    for word in query_words:
        if word in inverted_index:
            for doc, tfidf in inverted_index[word]:
                if doc == document:
                    document_vector[word] = tfidf

    # Compute dot product
    dot_product = sum(query_vector[word] * document_vector[word] for word in query_words)

    # Compute magnitudes
    query_magnitude = math.sqrt(sum(val**2 for val in query_vector.values()))
    document_magnitude = math.sqrt(sum(val**2 for val in document_vector.values()))

    if query_magnitude == 0 or document_magnitude == 0:
        return 0  # Avoid division by zero

    # Compute cosine similarity
    return dot_product / (query_magnitude * document_magnitude)

# Search function to compute and rank results
def search(query, dir_path):
    inverted_index = create_index(dir_path)
    tfidf_scores = {}
    cosine_scores = {}

    for filename in os.listdir(dir_path):
        if filename.endswith('.txt'):
            tfidf_scores[filename] = tf_idf(query, filename, inverted_index)
            cosine_scores[filename] = cosine_similarity(query, filename, inverted_index)

    # Rank documents
    ranked_tfidf = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=False)
    ranked_cosine = sorted(cosine_scores.items(), key=lambda x: x[1], reverse=False)

    return ranked_tfidf, ranked_cosine

# GUI class for the desktop application
class SearchEngineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Engine")
        self.root.geometry("800x600")

        # Select Directory
        self.dir_label = tk.Label(root, text="Select Directory for Documents:")
        self.dir_label.pack(pady=10)
        self.dir_button = tk.Button(root, text="Browse", command=self.select_directory)
        self.dir_button.pack()

        # Query Input
        self.query_label = tk.Label(root, text="Enter Search Query:")
        self.query_label.pack(pady=10)
        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack()

        # Search Button
        self.search_button = tk.Button(root, text="Search", command=self.perform_search)
        self.search_button.pack(pady=10)

        # Results Frame
        self.results_frame = ttk.Notebook(root)
        self.results_frame.pack(fill="both", expand=True, pady=10)

        self.tfidf_tab = tk.Text(self.results_frame, wrap=tk.WORD)
        self.cosine_tab = tk.Text(self.results_frame, wrap=tk.WORD)

        self.results_frame.add(self.tfidf_tab, text="TF-IDF Results")
        self.results_frame.add(self.cosine_tab, text="Cosine Similarity Results")

        self.dir_path = None

    def select_directory(self):
        self.dir_path = filedialog.askdirectory()
        if not self.dir_path:
            messagebox.showwarning("Warning", "Please select a valid directory.")

    def perform_search(self):
        if not self.dir_path:
            messagebox.showerror("Error", "No directory selected!")
            return

        query = self.query_entry.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a search query.")
            return

        try:
            tfidf_results, cosine_results = search(query, self.dir_path)
            self.display_results(self.tfidf_tab, tfidf_results, "TF-IDF")
            self.display_results(self.cosine_tab, cosine_results, "Cosine Similarity")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_results(self, text_widget, results, method):
        text_widget.delete(1.0, tk.END)
        if results:
            for doc, score in results:
                text_widget.insert(tk.END, f"{doc}: {score:.4f}\n")
        else:
            text_widget.insert(tk.END, f"No documents found using {method}.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchEngineApp(root)
    root.mainloop()
