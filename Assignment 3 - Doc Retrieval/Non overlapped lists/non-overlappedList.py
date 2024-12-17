import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')

# Initialize an empty dictionary to store document data
documents = {}

def tokenize_extract_nouns(content):
    # Initialize the lemmatizer and stop words
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    # Split the text into tokens
    tokens = word_tokenize(content)
    # Remove stop words and non-alphabetic characters
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    # Extract the nouns from the tokens
    nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos.startswith('N')]
    return nouns

def process_documents(directory):
    # Check if the folder path exists
    if os.path.exists(directory):
        # Iterate through the files in the folder
        for filename in os.listdir(directory):
            # Check if the file is a .txt file
            if filename.endswith(".txt"):
                # Construct the full path to the file
                file_path = os.path.join(directory, filename)
                print(f"Reading file: {file_path}")

                # Reading the content of the file
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    # Tokenize and extract nouns from the file content
                    nouns = tokenize_extract_nouns(file_content)

                    # Store the nouns in the documents dictionary
                    for noun in nouns:
                        if noun not in documents:
                            documents[noun] = set()  # Use set to store non-overlapping document lists
                        documents[noun].add(filename)  # Store the document in the set
        print("Dictionary successfully created")
    else:
        print("Invalid folder path. Please try again.")

def query_processing(user_query):
    # Tokenize and extract nouns from the user query
    query_nouns = tokenize_extract_nouns(user_query)
    return query_nouns

def retrieve_documents_per_term(query_nouns, documents):
    # Initialize an empty set to store non-overlapping results
    non_overlap_results = set()

    # Retrieve documents for each term and combine the sets
    for noun in query_nouns:
        if noun in documents:
            non_overlap_results.update(documents[noun])
    return non_overlap_results

def main():
    # Ask user for the folder path containing .txt files
    folder_path = input("Enter the folder path containing .txt files: ").strip()
    
    # Process the documents in the given folder
    process_documents(folder_path)

    if documents:
        # Get the user's query
        user_query = input("Enter your query: ")
        query_nouns = query_processing(user_query)
        non_overlap_results = retrieve_documents_per_term(query_nouns, documents)

        if non_overlap_results:
            print("Non-Overlapping Results:")
            for i, doc in enumerate(non_overlap_results):
                print(f"Document {i + 1}: {doc}")
        else:
            print("No relevant documents found.")
    else:
        print("No documents processed.")

if __name__ == "__main__":
    main()
