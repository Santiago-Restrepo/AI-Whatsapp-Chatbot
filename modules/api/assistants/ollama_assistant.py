from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
import json

class OllamaAssistant:
    def __init__(self, documents_mode='web'):
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

        # Create vector representation of documents for similarity search
        print("Creating vector representation of documents for similarity search...")
        self.vector = FAISS.from_documents(self.documents, self.embeddings)
        self.retriever = self.vector.as_retriever()

        print("Ollama Assistant initialized., #docs:", len(self.docs))

        

    def predict(self, question, conversation_history=[]):
        # Retrieve relevant documents based on the question
        retrieved_docs = self.retriever.invoke(question)
        formatted_context = self.combine_docs(retrieved_docs)
        
        # Generate response using the Ollama model
        formatted_prompt = f"Contexto: {formatted_context}\n\Pregunta: {question}\nRespuesta: "
        messages = [{'role': 'user', 'content': formatted_prompt}]
        if conversation_history:
            messages = conversation_history + messages
        response = ollama.chat(model='llama3',
                               messages=[{'role': 'user', 'content': formatted_prompt}],
                               options={'temperature': 0},
                               stream=True)
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
