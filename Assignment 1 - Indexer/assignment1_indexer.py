# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 11:01:59 2024

@author: Ayesha Nadeem
"""

import os
import re
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')

# Step 1: Define functions for document processing and noun indexing
def gather_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                documents.append({
                    'title': filename,
                    'content': content
                })
    return documents

def tokenize_extract_nouns(content):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(content)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos.startswith('N')]
    return nouns

def noun_indexer(documents):
    inverted_index = defaultdict(lambda: defaultdict(int))
    for doc in documents:
        doc_name = doc['title']
        paragraphs = doc['content'].split('\n\n')
        document_nouns = defaultdict(int)
        for paragraph in paragraphs:
            nouns = tokenize_extract_nouns(paragraph)
            paragraph_noun_counts = defaultdict(int)
            for noun in nouns:
                paragraph_noun_counts[noun.lower()] += 1
            for noun, count in paragraph_noun_counts.items():
                if count > 1:
                    document_nouns[noun] += count
        for noun, count in document_nouns.items():
            inverted_index[noun][doc_name] += count
    return inverted_index

def search_by_title(documents, query):
    results = []
    for doc in documents:
        if query.lower() in doc['title'].lower():
            results.append(doc)
    return results

def search_by_content(inverted_index, documents, query):
    nouns = tokenize_extract_nouns(query)
    matching_documents = defaultdict(int)
    for noun in nouns:
        if noun in inverted_index:
            for doc_name, count in inverted_index[noun].items():
                matching_documents[doc_name] += count
    ranked_documents = sorted(matching_documents.items(), key=lambda x: x[1], reverse=True)
    return ranked_documents

# Step 2: GUI Implementation with Tkinter
class DocumentSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Search Engine")
        self.root.geometry("600x500")
        
        # Document variables
        self.documents = []
        self.inverted_index = defaultdict(lambda: defaultdict(int))
        
        # GUI elements
        tk.Label(root, text="Document Search Engine", font=("Arial", 16)).pack(pady=10)
        
        # Buttons for folder selection and actions
        tk.Button(root, text="Load Documents", command=self.load_documents).pack(pady=5)
        
        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack(pady=5)
        
        tk.Button(root, text="Search by Title", command=self.search_by_title_gui).pack(pady=5)
        tk.Button(root, text="Search by Content", command=self.search_by_content_gui).pack(pady=5)
        
        # Results area
        self.result_text = scrolledtext.ScrolledText(root, width=70, height=20)
        self.result_text.pack(pady=10)
    
    def load_documents(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            messagebox.showwarning("Warning", "Please select a valid folder.")
            return
        
        self.documents = gather_documents(folder_path)
        self.inverted_index = noun_indexer(self.documents)
        messagebox.showinfo("Success", "Documents loaded and indexed successfully.")
    
    def search_by_title_gui(self):
        query = self.query_entry.get()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query.")
            return
        
        results = search_by_title(self.documents, query)
        self.display_results([(doc['title'], 0) for doc in results])
    
    def search_by_content_gui(self):
        query = self.query_entry.get()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query.")
            return
        
        ranked_results = search_by_content(self.inverted_index, self.documents, query)
        self.display_results(ranked_results)
    
    def display_results(self, ranked_documents):
        self.result_text.delete(1.0, tk.END)
        if not ranked_documents:
            self.result_text.insert(tk.END, "No matching documents found.\n")
            return
        
        for doc_name, relevance in ranked_documents:
            if relevance == 0:
                self.result_text.insert(tk.END, f"Title: {doc_name}\n")
                continue
            self.result_text.insert(tk.END, f"Title: {doc_name} (Occurrence: {relevance})\n")
            if doc_name in self.inverted_index:
                self.result_text.insert(tk.END, f"Nouns found in '{doc_name}':\n")
                for noun, count in self.inverted_index.items():
                    if doc_name in count:
                        self.result_text.insert(tk.END, f"{noun}: {count[doc_name]}\n")
            self.result_text.insert(tk.END, "=" * 50 + "\n")

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentSearchApp(root)
    root.mainloop()
