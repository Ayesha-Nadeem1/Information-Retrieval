# **Non-Overlapping Document Retrieval Model**

## Description

The **Non-Overlapping Document Retrieval Model** is designed to process text documents stored in a specified directory and retrieve relevant documents based on user queries. The model focuses on extracting nouns from both the documents and the user query, allowing for a targeted search. By employing a set data structure to store documents corresponding to each noun, the model ensures that the results returned for the user query do not contain overlapping entries, thus providing a unique list of relevant documents for each query.

## Features

- **Tokenization**: The model uses Natural Language Processing (NLP) techniques to tokenize the text, making it easier to analyze and extract specific words.
- **Lemmatization**: Words are lemmatized to reduce them to their base or dictionary form, improving matching accuracy.
- **Stop Words Removal**: Commonly used words that do not add significant meaning (stop words) are removed to focus on important terms.
- **Noun Extraction**: Only nouns are extracted from both documents and queries, narrowing down the search to more meaningful terms.
- **Non-Overlapping Results**: Documents are stored in sets, ensuring that each document appears only once in the results.

## Code Documentation

### Imports

```python
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
```
- **os**: Used for interacting with the operating system, particularly for file and directory management.
- **nltk**: The Natural Language Toolkit, a library for NLP tasks.

### NLTK Downloads

```python
nltk.download('punkt')
nltk.download('stopwords')
```
- Downloads necessary NLTK data files for tokenization and stop words.

### Global Variables

```python
documents = {}
```
- A global dictionary to store extracted nouns and their corresponding documents.

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

### Function: `process_documents(directory)`

```python
def process_documents(directory):
    ...
```
- **Input**: Path to the directory containing `.txt` files.
- **Output**: Updates the global `documents` dictionary.
- **Description**:
    - Iterates through `.txt` files in the specified directory.
    - Reads each file's content and extracts nouns using `tokenize_extract_nouns`.
    - Updates the `documents` dictionary with nouns as keys and sets of corresponding filenames as values.

### Function: `query_processing(user_query)`

```python
def query_processing(user_query):
    ...
```
- **Input**: A string representing the user query.
- **Output**: A list of nouns extracted from the query.
- **Description**: Utilizes the `tokenize_extract_nouns` function to extract relevant nouns from the user query.

### Function: `retrieve_documents_per_term(query_nouns, documents)`

```python
def retrieve_documents_per_term(query_nouns, documents):
    ...
```
- **Input**: List of nouns from the user query and the `documents` dictionary.
- **Output**: A set of non-overlapping document names that match the query.
- **Description**:
    - Initializes an empty set for storing unique document results.
    - For each noun in the query, it checks if the noun exists in the `documents` dictionary and adds the corresponding document names to the results.

### Function: `main()`

```python
def main():
    ...
```
- **Input**: None
- **Output**: None
- **Description**:
    - Prompts the user for the folder path containing `.txt` files.
    - Calls `process_documents` to process the files.
    - If documents are found, prompts the user for a query and retrieves non-overlapping results.
    - Displays the results or a message indicating no relevant documents were found.

### Entry Point

```python
if __name__ == "__main__":
    main()
```
- This block checks if the script is being run directly and calls the `main()` function to start the program.

## Data Flow Diagram

![](C:\Users\Ayesha Nadeem\AppData\Roaming\Typora\typora-user-images\image-20241008112938566.png)

## Usage Instructions

1. Ensure that the required `.txt` files are present in a specified folder.
2. Run the script in a Python environment where NLTK is installed and properly configured.
3. Input the folder path containing the `.txt` files when prompted.
4. Enter a query to retrieve non-overlapping document results based on extracted nouns.

## Conclusion

The **Non-Overlapping Document Retrieval Model** is an efficient way to process and retrieve documents based on user input, leveraging NLP techniques for improved search results. By ensuring that results are non-overlapping, it enhances the user experience by providing unique, relevant documents for each query.