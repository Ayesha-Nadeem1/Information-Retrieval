import networkx as nx
import os
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

def noun_indexer(documents, result, filename):
    for noun in result:
        if noun not in documents:
            documents[noun] = {}
        if filename not in documents[noun]:
            documents[noun][filename] = 0
        documents[noun][filename] += 1
    return documents


def tokenize_extract_nouns(content):
    # Initialize the lemmatizer and stop words
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    # Split the text into tokens
    tokens = word_tokenize(content)
    # Remove stop words and non-alphabetic characters
    tokens = [lemmatizer.lemmatize(
        token) for token in tokens if token.isalpha() and token not in stop_words]
    # Extract the nouns from the tokens
    nouns = [word for (word, pos) in nltk.pos_tag(
        tokens) if pos.startswith('N')]
    # print(nouns)
    return nouns

def read_text_files_in_folder(folder_path):

    print("Reading files in folder: " + folder_path)
    # Initialize an empty dictionary to store document data
    documents = {}

    # Check if the folder path exists
    if os.path.exists(folder_path):
        # Iterate through the files in the folder
        for filename in os.listdir(folder_path):
            # Check if the file is a .txt file
            if filename.endswith(".txt"):
                # Construct the full path to the file
                file_path = os.path.join(folder_path, filename)
                print(file_path)

                # Readng the content of the files and storing it in the documents list
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    # Add the nouns to the dictionary
                    result = tokenize_extract_nouns(file_content)
                    result = [res.lower() for res in result]
                    documents = noun_indexer(documents, result, filename)

    #print("Dictionary successfully created")
    print(documents)
    return documents

def build_subgraph(noun_dict, selected_keywords):
    G = nx.Graph()
    
    # Add selected keywords as nodes
    for keyword in selected_keywords:
        G.add_node(keyword, type='keyword')
    
    # Add files connected to selected keywords as nodes
    for keyword in selected_keywords:
        if keyword in noun_dict:
            files = noun_dict[keyword]
            for filename in files:
                G.add_node(filename, type='file')
    
    # Add edges between selected keywords and connected files
    for keyword in selected_keywords:
        if keyword in noun_dict:
            files = noun_dict[keyword]
            for filename in files:
                G.add_edge(keyword, filename)
    
    return G

def main():
    directory = 'C:\\Users\\Ayesha Nadeem\\OneDrive\\Documents\\semester 7\\IR\\Assignment 1 - Indexer\\Folder'
    noun_dict = read_text_files_in_folder(directory)

    while True:
        user_query = input("Enter your query (or 'q' to quit): ")

        if user_query.lower() == 'q':
            break

        res = tokenize_extract_nouns(user_query)
        
        if res:
            print(f'The user query "{res}" is connected to the following files:')
            
            # Build the graph for the selected keyword and connected files
            G = build_subgraph(noun_dict, res)
            
            # Draw the graph
            pos = nx.spring_layout(G, seed=42)
            node_colors = ['blue' if node in res else 'red' for node in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors)
            plt.show()
        else:
            print(f'The user query "{res}" was not found in any file.')

if __name__ == "__main__":
    main()
