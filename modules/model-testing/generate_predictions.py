import shutil
# Source and destination folders
source_folder = '../api/assistants/ollama_assistant'
destination_folder = './ollama_assistant'

# Copy the entire contents of the source folder to the destination folder
shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)

import json
import random
import os
from ollama_assistant import OllamaAssistant
from ollama_assistant.configurations import configurations


data_path = 'data'
def get_random_test_data(random_size):

  scraped_data_path = '../scraping/data/transformed.json'

  with open(scraped_data_path, 'r') as f:
    scraped_data = json.load(f)
  
  return random.sample(scraped_data, random_size)

def save_data(data, file_path):
  # Ask if data paht already exists
  if os.path.exists(file_path):
    print("File exists!")
    return
  with open(file_path, 'w') as f:
    json.dump(data,  f, indent=4)

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_predictions(assistant, test_data, conversation_history_mock, configuration):
  predictions_path = f"{data_path}/configuration_{configuration['id']}/predictions.json"
  predictions = []
  if os.path.exists(predictions_path):
     with open(predictions_path, 'r') as f:
      predictions = json.load(f)
  for data in test_data:
      # predict if it is not already predicted
      already_predicted = False
      for prediction in predictions:
          if prediction['prompt'] == data['prompt']:
              already_predicted = True
              break   
      if already_predicted:
          print(f"Prompt already predicted: {data['prompt']}")
          continue
      prediction = assistant.predict(data['prompt'], conversation_history = conversation_history_mock)
      new_data = {
      'prompt': data['prompt'],
      'reference': data['response'],
      'prediction': prediction
      }
      predictions.append(new_data)


      save_data(predictions, predictions_path)

if __name__ == '__main__':
    for configuration in configurations:
      try:
        create_directory_if_not_exists("data/configuration_" + configuration['id'])
        test_data = get_random_test_data(random_size=30)
        test_data_path = f"{data_path}/configuration_{configuration['id']}/test_data.json"
        save_data(test_data, test_data_path)
        assistant = OllamaAssistant(configuration=configuration)
        conversation_history_mock = [
            {
                'role': 'assistant',
                'content': 'Bienvenido al chatbot de la Personería Distrital De Medellín, la conversación finalizará una vez envíe la palabra finalizar o pasada 1 hora de haberse iniciado. ¿En qué podemos ayudarle el día de hoy?',
            }
        ]
        print(f"Test data loaded successfully for configuration {configuration['id']}")
        with open(test_data_path, 'r') as f:
            test_data = json.load(f)
            generate_predictions(assistant, test_data, conversation_history_mock, configuration)
        print(f"Predictions saved successfully for configuration {configuration['id']}")
      except Exception as e:
        print(f"Error: {e}")
        continue
    
    print('All predictions saved successfully')
