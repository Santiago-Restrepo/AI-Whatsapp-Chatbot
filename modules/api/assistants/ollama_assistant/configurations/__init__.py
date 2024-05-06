configurations = [
  {
    'id': '0',
    'format_prompt': lambda formatted_context, question: f"CONTEXTO -----\n\n({formatted_context})\n\n-----\n\nPregunta: {question}\n\nResponde de manera conscisa y corta: ",
    'chunk_size': 500,
    'chunk_overlap': 100,
    'vector_store': 'faiss',
    'embedding_model': 'nomic-embed-text',
  },
  {
    'id': '1',
    'format_prompt': lambda formatted_context, question: f"Responde la siguiente pregunta: {question}\n\nCONTEXTO -----\n\n({formatted_context})\n\n-----\n\n"
  },
  {
    'id': '2',
    'format_prompt': lambda formatted_context, question: f"Pregunta: {question}\n\nContexto: {formatted_context}\n\nRespuesta: "  
  },
    {
    'id': '3',
    'format_prompt': lambda formatted_context, question: f"Pregunta: {question}\n\nContexto: {formatted_context}\n\nPor favor, proporciona una respuesta precisa: "
  },
  {
    'id': '4',
    'format_prompt': lambda formatted_context, question: f"Considera el siguiente contexto:\n\n{formatted_context}\n\nAhora, responde la pregunta: {question}\n\nRespuesta: "
  },
  {
    'id': '5',
    'format_prompt': lambda formatted_context, question: f"Observa el siguiente escenario:\n\n{formatted_context}\n\nAhora, brinda una respuesta a la pregunta planteada: {question}\n\nTu respuesta: "
  },
  {
    'id': '6',
    'format_prompt': lambda formatted_context, question: f"Contexto:\n{formatted_context}\n\nPregunta:\n{question}\n\nPor favor, proporcione una respuesta concisa: "
  },
  {
    'id': '7',
    'format_prompt': lambda formatted_context, question: f"Explique cómo abordaría esta situación, dada la siguiente información:\n\n{formatted_context}\n\nPregunta: {question}\n\nRespuesta: "
  },
  {
    'id': '8',
    'format_prompt': lambda formatted_context, question: f"Antes de responder, considera el contexto siguiente:\n\n{formatted_context}\n\nAhora, responde la siguiente pregunta: {question}\n\nTu respuesta: "
  },
  {
    'id': '9',
    'format_prompt': lambda formatted_context, question: f"El siguiente contexto es relevante para la pregunta planteada:\n\n{formatted_context}\n\nPor favor, proporcione una respuesta a la pregunta: {question}\n\nRespuesta: "
  }
]