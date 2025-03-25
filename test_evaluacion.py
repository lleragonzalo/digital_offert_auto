import requests

url = "http://127.0.0.1:8000/evaluacion/10"
response = requests.post(url)

try:
    response_data = response.json()
    print("Respuesta del servidor:", response_data)
except requests.exceptions.JSONDecodeError:
    print("Error: La respuesta no es un JSON válido. Respuesta completa:", response.text)

