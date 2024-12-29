from flask import Flask, request, jsonify
import requests
import os
from prompt import gemini_prompt
app = Flask(__name__)

BASE_URL = {
    "gemini-1.5-flash-latest": {
        "URL": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=",
        "API_KEY": os.getenv('GEMINI_API_KEY'),
    }
}

@app.route('/askllm', methods=['POST'])
def askllm():
    resp = {}
    data = request.json
    metric_data = data.get('metrics')
    prompt = gemini_prompt(metric_data)
    response = requests.post(url=BASE_URL['gemini-1.5-flash-latest']['URL']+BASE_URL['gemini-1.5-flash-latest']['API_KEY'], json=prompt)
    if response.status_code != 200:
        resp['status'] = 'error'
        resp['message'] = 'Failed to get response from Gemini API'
        resp['replica_count'] = -1
        return jsonify(resp), 500
    print(response.json())
    replica_count = response.json().get('candidates')[0].get('content').get('parts')[0].get('text')
    replica_count = replica_count.replace("\n", "")
    resp['status'] = 'success'
    resp['message'] = 'Response from Gemini API'
    resp['replica_count'] = int(replica_count)
    print(resp)
    return jsonify(resp), 200

if __name__ == '__main__':
    app.run(debug=True) 