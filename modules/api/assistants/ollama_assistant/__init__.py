from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
import os
import pickle
from ollama_assistant.configurations import configurations
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
class OllamaAssistant:
    def __init__(self, configuration=configurations[0], vector_cached=False):
        self.configuration = configuration
        self.vector_chached = vector_cached
        self.load_and_save_documents()
        self.create_embeddings()
        self.create_vector_db()
        self.create_retriever()
    
    def load_and_save_documents(self):
        base_url = 'https://www.personeriamedellin.gov.co'
        paths = ['/servicios/preguntas-frecuentes/']
        web_paths = [base_url + path for path in paths]
        self.loader = WebBaseLoader(web_paths=web_paths)
        self.docs = self.loader.load()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.configuration['chunk_size'],
            chunk_overlap=self.configuration['chunk_overlap'],
            length_function=len,
        )
        self.documents = self.text_splitter.split_documents(self.docs)

    def create_embeddings(self):
        self.embeddings = OllamaEmbeddings(model=self.configuration['embedding_model'], show_progress=True)

    def create_vector_db(self):
        cache_file = 'cache/cached_vector.pkl'
        if os.path.exists(cache_file) and self.vector_chached:
            print("Loading cached vector representations...")
            with open(cache_file, 'rb') as f:
                self.vector = pickle.load(f)
            print("Cached vector representations loaded successfully.")
        else:
            print("Creating vector representations...")

            if self.configuration['vector_store'] == 'faiss':
                self.vector = FAISS.from_documents(self.documents, self.embeddings)

            elif self.configuration['vector_store'] == 'chroma':
                collection_name = f"chroma-collection-cfg{self.configuration['id']}"
                self.vector = Chroma.from_documents(documents=self.documents, collection_name=collection_name, embedding=self.embeddings)

            print("Vector representations created successfully.")
            # Save the vector representations to cache
            # with open(cache_file, 'wb') as f:
            #     pickle.dump(self.vector, f)

    def create_retriever(self):
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
