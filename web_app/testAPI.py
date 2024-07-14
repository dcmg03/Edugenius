import openai

# Configura tu clave API aquí
openai.api_key = 'clave'

# Realiza una solicitud de prueba
try:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    )
    print(completion.choices[0].message['content'])
except openai.error.OpenAIError as e:
    print(f"OpenAI API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
