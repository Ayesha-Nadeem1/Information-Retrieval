# **Proximal Nodes Document Indexing and Visualization Model**

## Description

The **Proximal Nodes Document Indexing and Visualization Model** is designed to analyze a set of text documents, extract nouns, and create a visual representation of the relationships between user-defined keywords and the documents in which they appear. The model employs a graph-based approach using NetworkX to illustrate connections, providing users with a clear understanding of how specific terms are related to the content of various documents.

## Features

- **Noun Extraction**: The model uses Natural Language Processing (NLP) techniques to identify and extract nouns from text documents.
- **Document Indexing**: Nouns are indexed with their respective document names and frequency of occurrence, allowing for efficient retrieval of related documents.
- **User Query Processing**: The model accepts user queries, extracts nouns from them, and finds connections to the indexed documents.
- **Graph Visualization**: The relationships between selected keywords and their corresponding documents are visualized using a graph, where keywords and documents are represented as nodes.

## Code Documentation

### Imports

```python
import networkx as nx
import os
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
```
- **networkx**: A library for creating and analyzing complex networks (graphs).
- **os**: Used for interacting with the operating system, particularly for file and directory management.
- **matplotlib.pyplot**: A plotting library used for visualizing data in graphical form.
- **nltk**: The Natural Language Toolkit, a library for NLP tasks.

### Function: `noun_indexer(documents, result, filename)`

```python
def noun_indexer(documents, result, filename):
    ...
```
- **Input**: 
  - `documents`: A dictionary storing nouns and their associated document information.
  - `result`: A list of extracted nouns from a document.
  - `filename`: The name of the document.
- **Output**: Updates the `documents` dictionary with the frequency of each noun in the document.
- **Description**: 
    - Iterates through the extracted nouns, updating their occurrence count for each document.

### Function: `tokenize_extract_nouns(content)`

```python
def tokenize_extract_nouns(content):
    ...
```
- **Input**: Text content from documents.
- **Output**: A list of extracted nouns from the content.
- **Description**: 
    - Initializes a lemmatizer and retrieves stop words.
    - Tokenizes the content into words.
    - Removes stop words and non-alphabetic characters.
    - Extracts nouns from the remaining tokens using part-of-speech tagging.

### Function: `read_text_files_in_folder(folder_path)`

```python
def read_text_files_in_folder(folder_path):
    ...
```
- **Input**: Path to the directory containing `.txt` files.
- **Output**: A dictionary of indexed nouns and their associated documents.
- **Description**:
    - Iterates through `.txt` files in the specified directory.
    - Reads each file's content and extracts nouns using `tokenize_extract_nouns`.
    - Updates the `documents` dictionary with nouns and their frequencies.

### Function: `build_subgraph(noun_dict, selected_keywords)`

```python
def build_subgraph(noun_dict, selected_keywords):
    ...
```
- **Input**: 
  - `noun_dict`: The dictionary of indexed nouns and documents.
  - `selected_keywords`: A list of keywords to be visualized.
- **Output**: A NetworkX graph object representing the connections.
- **Description**:
    - Creates a graph with selected keywords as nodes and their corresponding documents as connected nodes.
    - Adds edges between keywords and documents to illustrate their relationships.

### Function: `main()`

```python
def main():
    ...
```
- **Input**: None
- **Output**: None
- **Description**:
    - Prompts the user for a directory containing `.txt` files and reads them to create an indexed noun dictionary.
    - Accepts user queries and processes them to extract nouns.
    - Builds and visualizes a graph of relationships between the user-defined keywords and the documents they relate to.

### Entry Point

```python
if __name__ == "__main__":
    main()
```
- This block checks if the script is being run directly and calls the `main()` function to start the program.

## Data Flow Diagram

![image-20241008113646101](C:\Users\Ayesha Nadeem\AppData\Roaming\Typora\typora-user-images\image-20241008113646101.png)

## Usage Instructions

1. Ensure that the required `.txt` files are present in the specified folder.
2. Run the script in a Python environment where NLTK and NetworkX are installed and properly configured.
3. Input the folder path containing the `.txt` files when prompted.
4. Enter a query to retrieve proximal nodes related to the extracted nouns and visualize their connections.

## Conclusion

The **Proximal Nodes Document Indexing and Visualization Model** effectively combines text analysis and graph visualization to provide insights into the relationships between keywords and documents. This approach aids users in understanding content connectivity and enhances information retrieval processes, making it a valuable tool for document analysis and retrieval in various applications.