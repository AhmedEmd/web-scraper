from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import requests

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="llama3")


def parse_with_ollama(dom_chunks, parse_description):
    ollama_endpoint = "http://localhost:11434/api/generate"
    
    prompt = f"Parse the following HTML content according to this description: {parse_description}\n\nHTML Content:\n"
    for chunk in dom_chunks:
        prompt += chunk + "\n"

    try:
        response = requests.post(ollama_endpoint, json={
            "model": "llama2",  # or whichever model you're using
            "prompt": prompt
        })
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()['response']
    except requests.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return f"Error: Unable to connect to Ollama. Make sure the Ollama service is running and accessible. Details: {e}"