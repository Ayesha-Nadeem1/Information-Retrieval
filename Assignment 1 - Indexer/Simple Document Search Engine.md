Here’s a detailed documentation of the code, explaining each aspect and component thoroughly.

---

# Document Search Engine - Desktop Application Documentation

This application is a noun-based search engine that reads text files from a selected folder, indexes them based on noun occurrences, and allows users to search for documents either by title or content using nouns extracted from the query. It’s implemented using Python's **Tkinter** library for the GUI, with **NLTK** for text processing. 

## Requirements

- **Python 3.6 or later**
- **NLTK (Natural Language Toolkit)**

Before running the program, make sure to install the necessary libraries:
```bash
pip install nltk
```

NLTK requires some initial downloads for tokenization, lemmatization, and stopwords:
```python
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
```

## Code Structure

### Step 1: Importing Necessary Libraries

```python
import os
import re
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
```

1. **OS** and **RE** modules handle file I/O and regular expressions.
2. **NLTK** provides tools for text processing, like tokenization, lemmatization, stopword filtering, and part-of-speech tagging.
3. **Tkinter** modules (`tk`, `filedialog`, `messagebox`, `scrolledtext`) build the graphical interface for the desktop application.

---

### Step 2: Document Gathering Function

The `gather_documents` function reads `.txt` files in a specified directory and loads their content.

```python
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
```

- **Parameters**: `folder_path` (str) - Path to the folder containing `.txt` documents.
- **Returns**: A list of dictionaries with document `title` and `content`.

**Explanation**:
1. `os.listdir()` retrieves files in `folder_path`.
2. `.endswith(".txt")` filters only `.txt` files.
3. Each file’s content is read, stored in a dictionary with its filename as the title.

---

### Step 3: Tokenization and Noun Extraction Function

The `tokenize_extract_nouns` function processes the document content to extract nouns.

```python
def tokenize_extract_nouns(content):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(content)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos.startswith('N')]
    return nouns
```

- **Parameters**: `content` (str) - The text to process.
- **Returns**: A list of nouns.

**Explanation**:
1. **Tokenization**: `word_tokenize` splits text into words.
2. **Lemmatization**: Words are reduced to their base form.
3. **Filtering**: Stopwords and non-alphabetic tokens are removed.
4. **Noun Extraction**: `nltk.pos_tag` tags parts of speech, and only nouns are retained.

---

### Step 4: Noun Indexer Function

The `noun_indexer` function builds an inverted index, mapping each noun to documents where it appears.

```python
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
```

- **Parameters**: `documents` (list) - List of document dictionaries.
- **Returns**: An inverted index where each noun maps to document names and occurrence counts.

**Explanation**:
1. **Paragraph Splitting**: Content is split by double newlines.
2. **Noun Frequency**: Each noun's occurrences per paragraph are counted.
3. **Inverted Indexing**: Nouns are indexed with document names, only if they appear more than once in a paragraph.

---

### Step 5: Search Functions

#### Search by Title

```python
def search_by_title(documents, query):
    results = []
    for doc in documents:
        if query.lower() in doc['title'].lower():
            results.append(doc)
    return results
```

- **Parameters**: `documents` (list), `query` (str).
- **Returns**: A list of documents with titles matching the query.

#### Search by Content

```python
def search_by_content(inverted_index, documents, query):
    nouns = tokenize_extract_nouns(query)
    matching_documents = defaultdict(int)
    for noun in nouns:
        if noun in inverted_index:
            for doc_name, count in inverted_index[noun].items():
                matching_documents[doc_name] += count
    ranked_documents = sorted(matching_documents.items(), key=lambda x: x[1], reverse=True)
    return ranked_documents
```

- **Parameters**: `inverted_index`, `documents`, `query`.
- **Returns**: A list of documents with relevance scores based on noun matches.

---

### Step 6: GUI Class - DocumentSearchApp

The `DocumentSearchApp` class manages the Tkinter GUI for the search engine.

```python
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
        
        tk.Button(root, text="Load Documents", command=self.load_documents).pack(pady=5)
        
        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack(pady=5)
        
        tk.Button(root, text="Search by Title", command=self.search_by_title_gui).pack(pady=5)
        tk.Button(root, text="Search by Content", command=self.search_by_content_gui).pack(pady=5)
        
        self.result_text = scrolledtext.ScrolledText(root, width=70, height=20)
        self.result_text.pack(pady=10)
```

- **Constructor (`__init__`)**:
    - Initializes window dimensions and title.
    - Sets up document storage (`self.documents`) and index (`self.inverted_index`).
    - Adds labels, buttons, text entry, and scrolled text areas for user interaction.

#### Button Callbacks for Loading Documents and Search

1. **Load Documents**:
    ```python
    def load_documents(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            messagebox.showwarning("Warning", "Please select a valid folder.")
            return
        
        self.documents = gather_documents(folder_path)
        self.inverted_index = noun_indexer(self.documents)
        messagebox.showinfo("Success", "Documents loaded and indexed successfully.")
    ```
    - **Description**: Opens folder selection dialog, gathers documents, indexes them, and shows a success message.

2. **Search by Title**:
    ```python
    def search_by_title_gui(self):
        query = self.query_entry.get()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query.")
            return
        
        results = search_by_title(self.documents, query)
        self.display_results([(doc['title'], 0) for doc in results])
    ```

3. **Search by Content**:
    ```python
    def search_by_content_gui(self):
        query = self.query_entry.get()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query.")
            return
        
        ranked_results = search_by_content(self.inverted_index, self.documents, query)
        self.display_results(ranked_results)
    ```

### Display Results

```python
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
            self.result_text.insert(tk.END

, f"Content Preview: {self.inverted_index[doc_name]}\n")
        self.result_text.insert(tk.END, "-" * 40 + "\n")
```

---

### Running the Application

1. Instantiate the Tkinter root window.
2. Create an instance of the `DocumentSearchApp`.
3. Start the main event loop:

```python
if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentSearchApp(root)
    root.mainloop()
```

---

This documentation covers the code’s main functionality, file handling, text processing, GUI components, and search methods.

## Level 1 DFD

![](C:\Users\Ayesha Nadeem\OneDrive\Documents\semester 7\IR\Assignment 1 - Indexer\dfd.png)

## Level 2 DFD

![](C:\Users\Ayesha Nadeem\OneDrive\Documents\semester 7\IR\Assignment 1 - Indexer\Level2-DFD.png)