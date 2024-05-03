import shutil
# Source and destination folders
source_folder = '../api/assistants/ollama_assistant'
destination_folder = './ollama_assistant'

# Copy the entire contents of the source folder to the destination folder
shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)

import json
import os
import evaluate
from ollama_assistant.configurations import configurations

def get_predictions(directory_path):
  # Load all files inside data folder
  predictions = []
  for file in os.listdir(directory_path):
    if file.endswith('.json'):
      file_path = os.path.join(directory_path, file)
      with open(file_path, 'r') as f:
        predictions.extend(json.load(f))

  return predictions


def evaluate_predictions(test_predictions, results_path):
  
  metrics = ['rouge', 'bleu', 'chrf', 'ter', 'google_bleu', 'sacrebleu']

  for metric in metrics:
    metric = evaluate.load(metric)
    predictions = [prediction['prediction'] for prediction in test_predictions]
    references = [prediction['reference'] for prediction in test_predictions]
    
    results = metric.compute(predictions=predictions, references=references)
    
    save_evaluation_results(results, metric.name, results_path)

def save_evaluation_results(results, metric, results_path):

  with open(f'{results_path}/{metric}.json', 'w') as f:
    json.dump(results, f)

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

if __name__ == '__main__':
  for configuration in configurations:
    results_path = f"results/configuration_{configuration['id']}"
    predictions_path = f"data/configuration_{configuration['id']}"
    predictions = get_predictions(predictions_path)

    create_directory_if_not_exists(results_path)
    evaluate_predictions(predictions, results_path)
