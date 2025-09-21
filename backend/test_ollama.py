from ollama import Client
try:
    client = Client(host="http://localhost:11434")
    models = client.list()
    print("Available models:", models)
    # Test a simple chat request
    response = client.chat(model="gemma2:9b-instruct-q4_K_M", messages=[{"role": "user", "content": "Hello, world!"}])
    print("Chat Response:", response['message']['content'])
except Exception as e:
    print("Error:", e)