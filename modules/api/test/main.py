from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
import json
import os
import pickle
import random
import time

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
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
        formatted_prompt = f"CONTEXTO -----\n\n({formatted_context})\n\n-----\n\nPregunta: {question}\n\nResponde de manera conscisa y corta: "
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

data_path = 'data'
def select_test_data():

  scraped_data_path = './../../../modules/scraping/data/transformed.json'

  with open(scraped_data_path, 'r') as f:
    scraped_data = json.load(f)
  
  return random.sample(scraped_data, 30)

def load_test_data(data, timestamp):
  final_path = f"{data_path}/test_data_{timestamp}.json"
  with open(final_path, 'w') as f:
    json.dump(data,  f, indent=4)
  return final_path

if __name__ == '__main__':
    assistant = OllamaAssistant()


    test_attempts = 5
    conversation_history_mock = [
        {
            'role': 'assistant',
            'content': 'Bienvenido al chatbot de la Personería Distrital De Medellín, la conversación finalizará una vez envíe la palabra finalizar o pasada 1 hora de haberse iniciado. ¿En qué podemos ayudarle el día de hoy?',
        }
    ]

    for i in range(test_attempts):
        test_data = select_test_data()
        timestamp = time.time()
        timestamp = str(timestamp).replace('.', '')
        test_data_path = load_test_data(test_data, timestamp)
        print(f"Test data loaded successfully for attempt {i+1}")
        predictions_path = f"{data_path}/predictions_{timestamp}.json"
        with open(test_data_path, 'r') as f:
            test_data = json.load(f)

            predictions = []
            for data in test_data:
                # predict if it is not already predicted
                already_predicted = False
                for prediction in predictions:
                    if prediction['prompt'] == data['prompt']:
                        already_predicted = True
                        break   
                if already_predicted:
                    continue

                prediction = assistant.predict(data['prompt'], conversation_history = conversation_history_mock)
                new_data = {
                'prompt': data['prompt'],
                'reference': data['response'],
                'prediction': prediction
                }
                predictions.append(new_data)

                with open(predictions_path, 'w') as f:
                    json.dump(predictions, f, indent=4)
                
                print(f"Prediction for prompt: {data['prompt']} saved successfully")
    
    print('All predictions saved successfully')
