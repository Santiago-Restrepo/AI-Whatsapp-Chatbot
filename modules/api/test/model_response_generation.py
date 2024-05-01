from assistants import assistants
import json

assistant = assistants['ollama-assistant']()
data_path = './../../modules/api/test/data'
test_data_path = data_path + '/test_data.json'
conversationhistory_mock = [
  {
    'role': 'assistant',
    'body': 'Bienvenido al chatbot de la Personería Distrital De Medellín, la conversación finalizará una vez envíe la palabra finalizar o pasada 1 hora de haberse iniciado. ¿En qué podemos ayudarle el día de hoy?',
  }
]
with open(test_data_path, 'r') as f:
  test_data = json.load(f)

  predictions = []
  for data in test_data:
    prediction = assistant.predict(data['prompt'], conversation_history = conversationhistory_mock)
    new_data = {
      'prompt': data['prompt'],
      'reference': data['response'],
      'prediction': prediction
    }
    predictions.append(new_data)

    with open(data_path + '/predictions.json', 'w') as f:
      json.dump(predictions, f, indent=4)
  