import pandas as pd
import matplotlib.pyplot as plt

# Function to load CSV file and visualize all results
def visualize_results(metric):
  csv_file = f'tabulated_results/{metric}.csv'
  save_path = f'visualized_results/{metric}.png'

  df = pd.read_csv(csv_file)
  df.set_index('configuration_name').plot(kind='line', marker='o')
  plt.xlabel('Configuration')
  plt.ylabel('Metric Value')
  plt.title(f"'{metric}' Performance Across Configurations")
  plt.xticks(rotation=45)
  plt.legend(title='Metric')
  if save_path:
    plt.savefig(save_path)
  else:
    plt.show()

# # Load and visualize all results from 'all.csv'
# visualize_results('tabulated_results/all.csv', 'visualized_results/all.png')

# Load and visualize individual results from 'bert_score.csv'
visualize_results('bert_score')

# # Load and visualize individual results from 'bleu.csv'
visualize_results('bleu')

# # Load and visualize individual results from 'rouge.csv'
visualize_results('rouge')
