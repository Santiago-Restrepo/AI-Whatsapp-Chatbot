import json
import os
import evaluate


data_path = 'data'

def load_predictions():
  # Load all files inside data folder
  predictions = []
  for file in os.listdir(data_path):
    if file.endswith('.json'):
      file_path = os.path.join(data_path, file)
      with open(file_path, 'r') as f:
        predictions.extend(json.load(f))

  return predictions


def evaluate_predictions(test_predictions):
  
  metrics = ['rouge', 'bleu', 'chrf', 'ter', 'google_bleu', 'sacrebleu']

  for metric in metrics:
    metric = evaluate.load(metric)
    predictions = [prediction['prediction'] for prediction in test_predictions]
    references = [prediction['reference'] for prediction in test_predictions]
    
    results = metric.compute(predictions=predictions, references=references)
    
    save_evaluation_results(results, metric.name)

def save_evaluation_results(results, metric):

  with open(f'results/{metric}.json', 'w') as f:
    json.dump(results, f)

if __name__ == '__main__':
  predictions = load_predictions()
  evaluate_predictions(predictions)
