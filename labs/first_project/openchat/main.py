import gradio as gr
import requests
import json

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

conversation_history = [] # may reach the token limit, create a history limiter

def generate_response(prompt):
    
    conversation_history.append(prompt)
    full_prompt = "\n".join(conversation_history)

    data = {
        "model": "mistral",
        "stream": False,
        "prompt": full_prompt
    }
 
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        text_response = data["response"]
        conversation_history.append(text_response)
        return text_response
    else:
        return "Error"

iface = gr.Interface(
    fn=generate_response, 
    inputs=gr.Textbox(lines=2, placeholder="enter your prompt here"), 
    outputs=["text"], 
)

iface.launch()