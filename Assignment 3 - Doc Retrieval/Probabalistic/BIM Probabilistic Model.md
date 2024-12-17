### **Documentation of Text Search System Using BIM Probabilistic Model**

---

#### Overview:
This Python script is a text retrieval system that ranks documents based on their relevance to a user's query. It uses natural language processing (NLP) techniques to preprocess text and the **Binary Independence Model (BIM)**, a probabilistic retrieval model, to rank the documents based on Jaccard similarity. The system processes `.txt` files in a folder and allows a user to search for relevant documents using a query, extracting key words from both the documents and the query for comparison.

---

### Key Features:
- Tokenization of both the user query and documents to extract meaningful words (nouns and adjectives).
- Removal of stopwords (common words that do not carry significant meaning).
- Calculation of document similarity using the **Jaccard similarity** metric.
- Ranking of documents using the **Binary Independence Model (BIM)** probabilistic retrieval method.
- Displays the top-K most relevant documents to the user.

---

### Components of the Script:

1. **Libraries Used:**
   - `os`: For interacting with the filesystem (e.g., reading `.txt` files).
   - `nltk`: For Natural Language Processing tasks (tokenization, lemmatization, stopwords removal, POS tagging).
     - **Stopwords**: Commonly used words (e.g., "the", "is") that are filtered out to focus on meaningful content.
     - **WordNetLemmatizer**: Reduces words to their base forms (e.g., "running" to "run").
     - **POS Tagging**: Used to identify and extract only the nouns (N) and adjectives (J) from the tokenized content.

2. **Functions:**
   - **`tokenize_extract_words(content)`**:
     - This function preprocesses the text by:
       1. Tokenizing the content into words.
       2. Removing stopwords and non-alphabetical tokens.
       3. Lemmatizing the words.
       4. Extracting only nouns and adjectives.
   - **`query_processing(user_query)`**:
     - Preprocesses the user query using the same steps as document preprocessing, to ensure a uniform comparison.
   - **`jaccard_similarity(set1, set2)`**:
     - Computes the Jaccard similarity between two sets of words. The Jaccard index is defined as the size of the intersection divided by the size of the union of two sets.
     - Formula: 
       \[
       \text{Jaccard Similarity} = \left( \frac{|A \cap B|}{|A \cup B|} \right) \times 100
       \]
   - **`bim_probabilistic_ranking(query_words, documents)`**:
     - Implements the **Binary Independence Model (BIM)** for probabilistic retrieval. It calculates the similarity between the query and each document using Jaccard similarity.
     - Documents are ranked based on similarity scores, and the top results are returned.

3. **Execution Flow:**
   - **Step 1**: The user is prompted to enter the folder path containing `.txt` files.
   - **Step 2**: The program reads all the `.txt` files in the folder, preprocesses each document, and stores the extracted words.
   - **Step 3**: The user is prompted to enter a search query, which is also preprocessed.
   - **Step 4**: Using the BIM model, the system ranks the documents based on their similarity to the query.
   - **Step 5**: The top-K most relevant documents are displayed to the user along with their similarity scores.

---

### Explanation of the Probabilistic Model: **Binary Independence Model (BIM)**

The **Binary Independence Model (BIM)** is a popular probabilistic model used in Information Retrieval. It ranks documents based on the probability that a document is relevant to the user’s query. The model operates under several key assumptions:
1. **Binary Representation**: Words are represented in binary form — either they appear in the document or they do not.
2. **Independence**: It assumes the presence or absence of a word in a document is independent of the presence or absence of any other word.
3. **Relevance Probability**: The model calculates the probability of relevance of each document based on the query terms.

#### Formula:
The BIM ranks documents based on the probability \( P(R|D) \), which is the probability that the document \( D \) is relevant to the query \( R \). However, in this simplified approach, the Jaccard similarity serves as a proxy to estimate this probability, where the intersection of words between the query and document gives a measure of similarity.

The **Jaccard similarity** is used here to calculate the overlap between the set of words in the query and the set of words in each document. This helps determine how "relevant" each document is to the query based on shared content (nouns and adjectives).

---

### How BIM Works in This Code:
1. **Query and Document Representation**: 
   - Both the query and documents are represented as sets of words (specifically nouns and adjectives), which reflect the content most likely relevant for matching.
   
2. **Ranking Mechanism**: 
   - The system computes the Jaccard similarity between the query set and the set of words in each document.
   - Higher overlap between the query and document words leads to a higher score, ranking that document as more relevant.

---

### Example Execution:

1. **Input**:
   - Folder path: `./documents/`
   - User query: `"machine learning in healthcare"`

2. **Preprocessing**:
   - Query processing extracts key terms like: `['machine', 'learning', 'healthcare']`
   - Documents are also processed, extracting their key nouns and adjectives.

3. **Ranking**:
   - For each document, the system calculates the Jaccard similarity between the query terms and the document terms.
   - Documents are ranked based on their similarity scores, with the top 5 being displayed to the user.

4. **Output**:
   ```
   Rank 1: 'document1.txt' - Similarity Score: 75.00
   Rank 2: 'document3.txt' - Similarity Score: 65.00
   Rank 3: 'document5.txt' - Similarity Score: 50.00
   ```

---

### Data Flow Diagram

![image-20241008113237016](C:\Users\Ayesha Nadeem\AppData\Roaming\Typora\typora-user-images\image-20241008113237016.png)

---

### Conclusion:
This text retrieval system provides a simple yet effective way to search documents based on a query. By leveraging the **Binary Independence Model (BIM)** with Jaccard similarity, it ranks documents based on the overlap of important words between the query and the documents. It is an excellent starting point for text retrieval tasks, offering a foundation that can be extended with more advanced retrieval and ranking techniques.