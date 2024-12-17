import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')

# Function to tokenize, remove stop words, and extract nouns and adjectives
def tokenize_extract_words(content):
    # Initialize lemmatizer and stop words
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    # Tokenize and remove non-alphabetical characters
    tokens = word_tokenize(content.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    
    # Extract nouns and adjectives using part-of-speech tagging
    words = [word for word, pos in nltk.pos_tag(tokens) if pos.startswith('N') or pos.startswith('J')]  # Include Nouns (N) and Adjectives (J)
    return words

# Function to process user query by tokenizing and extracting words (nouns + adjectives)
def query_processing(user_query):
    query_words = tokenize_extract_words(user_query)
    return query_words

# Function to calculate Jaccard similarity between two sets
def jaccard_similarity(set1, set2):
    if not set1 or not set2:
        return 0.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return (intersection / union) * 100

# Function to rank documents based on BIM probabilistic retrieval
def bim_probabilistic_ranking(query_words, documents):
    document_scores = {}
    for doc, doc_words in documents.items():
        score = jaccard_similarity(set(query_words), doc_words)
        document_scores[doc] = score
    
    # Sort documents by score in descending order
    ranked_documents = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_documents

def main():
    # Ask user for the folder path containing .txt files
    folder_path = input("Enter the folder path containing .txt files: ").strip()
    
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print("Invalid folder path. Please try again.")
        return
    
    # Initialize dictionary to store document content
    documents = {}
    
    # Iterate through all .txt files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                words = tokenize_extract_words(content)
                documents[filename] = set(words)
    
    if not documents:
        print("No valid .txt files found in the specified folder.")
        return
    
    # Get the user's query
    user_query = input("Enter your search query: ").strip()
    
    # Process the user's query to extract nouns and adjectives
    query_words = query_processing(user_query)
    
    # Rank the documents based on BIM probabilistic retrieval
    ranked_documents = bim_probabilistic_ranking(query_words, documents)
    
    # Display the top-K results (K = 5 in this case)
    if ranked_documents:
        K = min(5, len(ranked_documents))  # Show top 5 or fewer if fewer documents are available
        
        for i, (doc, score) in enumerate(ranked_documents[:K]):
            print(f"Rank {i + 1}: '{doc}' - Similarity Score: {score:.2f}")
    else:
        print("No relevant documents found.")

if __name__ == "__main__":
    main()
