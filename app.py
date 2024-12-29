from flask import Flask
import requests
from prompt import gemini_prompt
app = Flask(__name__)

BASE_URL = {
    "gemini-1.5-flash-latest": {
        "URL": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=",
        "API_KEY": "",
    }
}

@app.route('/askllm', methods=['POST'])
def askllm():
    data = request.json
    metric_data = data.get('metrics')
    prompt = gemini_prompt(metric_data)
    response = requests.post(url=BASE_URL['gemini-1.5-flash-latest']['URL']+BASE_URL['gemini-1.5-flash-latest']['API_KEY'], json=prompt)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True) 