import pandas as pd
import numpy as np
from ollama_assistant.configurations import configurations
import json


def extract_metric_results(results, metric, configuration_name):
  if metric == 'bert_score':
    return {
      'configuration_name': configuration_name,
      'bert_score_avg_precision': np.mean(results['precision']),
      'recall': np.mean(results['recall']),
      'f1': np.mean(results['f1'])
    }
  
  if metric == 'bleu':
    return {
      'configuration_name': configuration_name,
      'bleu': results['bleu'],
      'bleu_avg_precision': np.mean(results['precisions']),
    }
  if metric == 'rouge':
    return {
      'configuration_name': configuration_name,
      'rouge1': results['rouge1'],
      'rouge2': results['rouge2'],
      'rougeL': results['rougeL'],
      'rougeLsum': results['rougeLsum']
    }

def main():
  results = []
  metrics = ['bleu', 'rouge', 'bert_score']
  metric_tabulated_results = {metric: [] for metric in metrics}

  for configuration in configurations:
    configuration_name = f"cfg_{configuration['id']}"
    base_path = f'results/configuration_{configuration["id"]}'
    configuration_results = {'configuration_name': configuration_name}
    for metric in metrics:
      with open(f'{base_path}/{metric}.json', 'r') as f:
        metric_results = json.load(f)
      metric_results = extract_metric_results(metric_results, metric, configuration_name)
      metric_tabulated_results[metric].append(metric_results)
      configuration_results.update(metric_results)
    results.append(configuration_results)

  df = pd.DataFrame(results)
  df.to_csv('tabulated_results/all.csv', index=False)

  for metric in metrics:
    df = pd.DataFrame(metric_tabulated_results[metric])
    df.to_csv(f'tabulated_results/{metric}.csv', index=False)

if __name__ == '__main__':
    main()
