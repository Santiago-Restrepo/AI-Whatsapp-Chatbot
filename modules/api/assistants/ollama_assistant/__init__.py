from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
import json
import os
import pickle
from ollama_assistant.configurations import configurations
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
class OllamaAssistant:
    def __init__(self, documents_mode='web', configuration=configurations[0]):
        self.configuration = configuration
        self.embeddings = OllamaEmbeddings(model='llama3')
        # Load documents from the web or from JSON files based on the provided paths
        if documents_mode == 'web':
            base_url = 'https://www.personeriamedellin.gov.co'
            paths = ['/servicios/preguntas-frecuentes/']
            web_paths = [base_url + path for path in paths]
            self.loader = WebBaseLoader(web_paths=web_paths)
            self.docs = self.loader.load()
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=80,
                length_function=len,
            )
            self.documents = self.text_splitter.split_documents(self.docs)
        elif documents_mode == 'json':
            file_path = 'data/transformed.json'
            with open(file_path, 'r', encoding='utf-8') as file:
                self.docs = json.load(file)
        else:
            raise ValueError("Invalid documents_mode. Must be 'web' or 'json'")
        
                # Check if cached vector representations exist
        cache_file = 'cache/cached_vector.pkl'
        if os.path.exists(cache_file):
            print("Loading cached vector representations...")
            with open(cache_file, 'rb') as f:
                self.vector = pickle.load(f)
            print("Cached vector representations loaded successfully.")
        else:
            print("Creating vector representation of documents...")
            self.vector = FAISS.from_documents(self.documents, self.embeddings)
            # Save the vector representations to cache
            with open(cache_file, 'wb') as f:
                pickle.dump(self.vector, f)
            print("Vector representation of documents created and cached successfully.")

        self.retriever = self.vector.as_retriever()


        

    def predict(self, question, conversation_history=[]):
        # Retrieve relevant documents based on the question
        print("Retrieving relevant documents...")
        retrieved_docs = self.retriever.invoke(question)
        formatted_context = self.combine_docs(retrieved_docs)
        print(len(retrieved_docs), "relevant documents retrieved successfully")
        
        # Generate response using the Ollama model
        formatted_prompt = self.configuration['format_prompt'](question, formatted_context)
        messages = [{'role': 'user', 'content': formatted_prompt}]
        if conversation_history:
            messages = conversation_history + messages
        response = ollama.chat(model='llama3',
                               messages=messages,
                               options={'temperature': 0})
        return response['message']['content']

    def combine_docs(self, docs):
        # Combine the text content of retrieved documents
        return "\n\n".join(doc.page_content for doc in docs)
    
    def get_conversation_history(self, messages):
        formatted_messages = []

        for msg in messages:
            formatted_messages.append({'role': 'user', 'content': msg.body})
            formatted_messages.append({'role': 'assistant', 'content': msg.response})

        return formatted_messages
