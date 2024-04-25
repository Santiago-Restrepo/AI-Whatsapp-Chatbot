def extract_final_response(generated_text, response_separator='[/INST]'):
    # Split the generated text using the response separator
    segments = generated_text.split(response_separator)
    # Return the last segment, which should contain the new response
    final_response = segments[-1].strip()
    # Remove any trailing </s> tags
    final_response = final_response.rstrip('</s>')
    return final_response

# Example usage:
generated_text = """
<s>[INST] Qué es la personería de Medellín? [/INST] <s>[INST] Hola [/INST] Bienvenido al chatbot de la Personería Distrital De Medellín, nuestra conversación finalizará una vez envíes la palabra *finalizar* o pasadas 72 horas de haberse iniciado. ¿En qué puedo ayudarte el día de hoy?</s> <s>[INST] Qué es la personería de Medellín? [/INST] La Personería Distrital de Medellín es el encargado de velar por el cumplimiento de la ley y la Constitución en el Distrito.</s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></s></</s> 
"""

final_response = extract_final_response(generated_text)
print(final_response)