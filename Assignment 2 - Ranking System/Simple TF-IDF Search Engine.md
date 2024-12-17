# 								Simple TF-IDF Search Engine

This task implements a basic search engine using **TF-IDF (Term Frequency-Inverse Document Frequency)** algorithm for document relevance. It processes a directory of text files, builds an inverted index from them, and calculates the TF-IDF scores for search queries provided by the user. The search engine then ranks the documents based on their relevance to the query.

---

## **Concepts Used in the Code**

### **1. Natural Language Processing (NLP)**

- **Tokenization**: Splits a string of text into individual words (tokens).  
  - The `word_tokenize` function from NLTK is used to tokenize text into words.
- **Part-of-Speech (POS) Tagging**: Identifies the grammatical role of words (e.g., noun, verb).  
  - `nltk.pos_tag` assigns a part-of-speech tag to each word in a tokenized document.
- **Stopword Removal**: Removes common words like "the", "and", "is", which do not add meaning to document similarity.  
  - Stopwords are filtered using the `stopwords` corpus from NLTK.

---

### **2. TF-IDF (Term Frequency-Inverse Document Frequency)**

#### **How it Works**
TF-IDF is a statistical method used to evaluate how important a word is to a document in a collection (or corpus).

- **Steps**:
  1. **Term Frequency (TF)**:
     
     - Measures how often a term (word) appears in a document.  
       Formula:  
       $$
       TF = \frac{\text{Number of times term \( t \) appears in document}}{\text{Total number of terms in document}}
       $$
     
  2. **Inverse Document Frequency (IDF)**:
     - Measures how rare a term is across all documents in the collection.  
       Formula:  
       $$
       IDF = \log\left(\frac{\text{Total number of documents} + 1}{\text{Number of documents containing term \( t \)} + 1}\right) + 1
       $$
       - Adding 1 to both numerator and denominator avoids division by zero.
  
  3. **TF-IDF Score**:
     - Combines TF and IDF to score each term in a document:  
       $$
       TF-IDF = TF \times IDF
       $$

#### **Usage in the Code**
- Each word in a document is assigned a TF-IDF score.
- The scores are stored in an **inverted index**, which maps words to the list of documents and their corresponding TF-IDF scores.
- The `create_index` function generates the inverted index for all documents.

---

### **3. Cosine Similarity**

#### **How it Works**
Cosine similarity is a metric used to determine how similar two documents are, irrespective of their size, by measuring the cosine of the angle between their vector representations.

- **Vector Representation**:
  - The query and each document are represented as vectors, where:
    - Each dimension corresponds to a unique term.
    - Term weights in the vector are derived from TF-IDF scores.

- **Formula**:
  \[
  \text{Cosine Similarity} = \frac{\text{Dot Product of Query and Document Vectors}}{\text{Magnitude of Query Vector} \times \text{Magnitude of Document Vector}}
  \]

  - **Dot Product**:
    \[
    \text{Dot Product} = \sum_{i=1}^n \text{(Query Vector Term Weight)}_i \times \text{(Document Vector Term Weight)}_i
    \]

  - **Magnitude**:
    \[
    \text{Magnitude of Vector} = \sqrt{\sum_{i=1}^n (\text{Term Weight})_i^2}
    \]

#### **Steps**:
1. Tokenize and preprocess the query and documents.
2. Generate TF-IDF vectors for the query and documents.
3. Compute the dot product and magnitudes of the vectors.
4. Divide the dot product by the product of magnitudes to compute similarity.

#### **Usage in the Code**
- The `cosine_similarity` function calculates the similarity score for the query and each document.
- Both query and document are processed using the `preprocess` function.
- The TF-IDF values are retrieved from the inverted index.

---

### **4. Inverted Index**

- A data structure that maps words to the list of documents containing them, along with metadata such as TF-IDF scores.
- Efficient for searching and retrieving documents based on terms.

---

## **How the Program Works**

1. **Document Preprocessing**:
   - Load and preprocess all text documents in the selected directory.  
   - Tokenize, remove stopwords, and extract nouns using POS tagging.

2. **Index Creation**:
   - Build an inverted index mapping words to documents and their TF-IDF scores using `create_index`.

3. **Search Query Handling**:
   - Preprocess the query in the same manner as the documents.
   - Compute scores for each document:
     - **TF-IDF**: Sum of TF-IDF values for all query terms in a document.
     - **Cosine Similarity**: Calculate similarity based on vector representation.

4. **Ranking Results**:
   - Rank documents based on their TF-IDF and Cosine Similarity scores.

5. **Displaying Results**:
   - Present ranked results in the GUI using a tabbed interface.

---

### **Limitations**
1. Only considers nouns during preprocessing, which may exclude relevant terms.
2. Assumes documents are in plain text format (.txt).
3. Limited to single-word queries; multi-word queries are treated as individual terms.

---

### **Summary**
This program demonstrates a basic search engine implementation combining **TF-IDF** and **Cosine Similarity**. It preprocesses documents, builds an inverted index, and ranks documents based on relevance to a query. The GUI provides an easy-to-use interface for document selection and displaying ranked results.