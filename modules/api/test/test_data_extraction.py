import json
import random

def select_test_data():

  scraped_data_path = './../../modules/scraping/data/transformed.json'

  with open(scraped_data_path, 'r') as f:
    scraped_data = json.load(f)
  
  return random.sample(scraped_data, 30)

def load_test_data(data):
  with open('./../../modules/api/test/data/test_data.json', 'w') as f:
    json.dump(data, f)

test_data = select_test_data()
load_test_data(test_data)


