import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from collections import defaultdict

# Download required NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

class DocumentRetrievalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Retrieval App")
        self.root.geometry("400x500")
        self.folder_path = ""
        self.inverted_index = defaultdict(set)
        self.document_terms = {}

        # Create UI elements
        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="Document Retrieval System", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self.root, text="Select Folder", command=self.select_folder, width=20).pack(pady=5)

        self.folder_label = tk.Label(self.root, text="No folder selected.", font=("Arial", 12))
        self.folder_label.pack(pady=5)

        tk.Button(self.root, text="Non-Overlapping Retrieval", command=self.non_overlapping_retrieval, width=30).pack(pady=5)
        tk.Button(self.root, text="Probabilistic Retrieval", command=self.probabilistic_retrieval, width=30).pack(pady=5)
        tk.Button(self.root, text="Proximal Nodes Retrieval", command=self.proximal_node_retrieval, width=30).pack(pady=5)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            self.folder_label.config(text=f"Selected Folder: {folder}")
            self.process_documents(folder)
        else:
            self.folder_label.config(text="No folder selected.")

    def preprocess_text(self, text, include_adjectives=False):
        """
        Preprocess text by tokenizing, lemmatizing, and filtering
        """
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        
        # Tokenize and lowercase
        tokens = word_tokenize(text.lower())
        
        # Remove non-alphabetic tokens and stopwords
        tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
        
        # Lemmatize tokens
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        
        # Add POS tagging for filtering
        pos_tags = nltk.pos_tag(tokens)
        
        # Filter tokens based on POS
        if include_adjectives:
            filtered_tokens = [word for word, pos in pos_tags 
                               if pos.startswith('N') or pos.startswith('J')]
        else:
            filtered_tokens = [word for word, pos in pos_tags 
                               if pos.startswith('N')]
        
        return filtered_tokens

    def process_documents(self, directory):
        """
        Process documents in the given directory and create an inverted index
        """
        self.inverted_index.clear()
        self.document_terms.clear()
        
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Invalid folder path.")
            return
        
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        # Extract terms with adjectives
                        terms = self.preprocess_text(content, include_adjectives=True)
                        
                        # Store document terms
                        self.document_terms[filename] = set(terms)
                        
                        # Create inverted index
                        for term in terms:
                            self.inverted_index[term].add(filename)
                except Exception as e:
                    messagebox.showwarning("Warning", f"Could not process {filename}: {str(e)}")

    def non_overlapping_retrieval(self):
        """
        Non-Overlapping Retrieval: Retrieve documents for multiple query terms
        """
        if not self.inverted_index:
            messagebox.showerror("Error", "No documents processed.")
            return
        
        # Get user query
        query = simpledialog.askstring("Query", "Enter search terms (comma-separated):")
        if not query:
            return
        
        # Preprocess query terms
        query_terms = [term.strip().lower() for term in query.split(',')]
        query_terms = self.preprocess_text(' '.join(query_terms))
        
        # Retrieve documents for each term
        results = set()
        for term in query_terms:
            if term in self.inverted_index:
                results.update(self.inverted_index[term])
        
        # Display results
        self.display_results("Non-Overlapping Retrieval", 
                             "\n".join(sorted(results)) if results else "No documents found.")

    def probabilistic_retrieval(self):
        """
        Probabilistic Retrieval using Binary Independence Model (BIM)
        """
        if not self.inverted_index:
            messagebox.showerror("Error", "No documents processed.")
            return
        
        # Get user query
        query = simpledialog.askstring("Query", "Enter search query:")
        if not query:
            return
        
        # Preprocess query
        query_terms = self.preprocess_text(query, include_adjectives=True)
        
        # Calculate document scores using Jaccard coefficient
        document_scores = {}
        for doc, doc_terms in self.document_terms.items():
            # Calculate Jaccard similarity
            query_term_set = set(query_terms)
            doc_term_set = set(doc_terms)
            
            intersection = len(query_term_set & doc_term_set)
            union = len(query_term_set | doc_term_set)
            
            # Calculate similarity score
            similarity = (intersection / union) * 100 if union > 0 else 0
            document_scores[doc] = similarity
        
        # Sort and rank documents
        ranked_results = sorted(document_scores.items(), 
                                key=lambda x: x[1], 
                                reverse=True)
        
        # Format results
        results = "\n".join([f"Rank {i+1}: {doc} - Score: {score:.2f}%" 
                             for i, (doc, score) in enumerate(ranked_results) 
                             if score > 0])
        
        # Display results
        self.display_results("Probabilistic Retrieval", 
                             results if results else "No relevant documents found.")

    def proximal_node_retrieval(self):
        """
        Proximal Nodes Retrieval: Create a graph of related documents
        """
        if not self.inverted_index:
            messagebox.showerror("Error", "No documents processed.")
            return
        
        # Get user query
        query = simpledialog.askstring("Query", "Enter keywords for proximal nodes:")
        if not query:
            return
        
        # Preprocess query terms
        query_terms = self.preprocess_text(query)
        
        # Create graph
        G = nx.Graph()
        
        # Add query terms as nodes
        for term in query_terms:
            G.add_node(term, type='keyword')
            
            # Connect to documents containing the term
            if term in self.inverted_index:
                for doc in self.inverted_index[term]:
                    G.add_node(doc, type='document')
                    G.add_edge(term, doc)
        
        # Visualize graph
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, seed=42)
        
        # Color nodes based on type
        node_colors = ['blue' if G.nodes[node]['type'] == 'keyword' else 'red' 
                       for node in G.nodes()]
        
        nx.draw(G, pos, with_labels=True, 
                node_color=node_colors, 
                font_size=10, 
                node_size=500, 
                font_weight='bold')
        plt.title("Proximal Nodes Retrieval")
        plt.show()

    def display_results(self, method, results):
        """
        Display retrieval results in a new window
        """
        result_window = tk.Toplevel(self.root)
        result_window.title(f"{method} Results")
        result_window.geometry("600x400")
        
        text = tk.Text(result_window, wrap="word", width=80, height=20, font=("Arial", 12))
        text.insert("1.0", results)
        text.config(state="disabled")
        
        scrollbar = tk.Scrollbar(result_window, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        text.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def main():
    root = tk.Tk()
    app = DocumentRetrievalApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()