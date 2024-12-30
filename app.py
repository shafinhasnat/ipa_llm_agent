from flask import Flask, request, jsonify
from llm import LLM, Prompt
import os
app = Flask(__name__)

API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_NAME = "gemini-1.5-flash"

@app.route('/askllm', methods=['POST'])
def askllm():
    resp = {}
    data = request.json
    metric_data = data.get('metrics')
    prompt = Prompt(metric_data).prompt_builder()
    llm = LLM(api_key=API_KEY, model=MODEL_NAME)
    response = llm.ask(prompt)
    if response.get('status') != "success":
        resp['status'] = 'error'
        resp['message'] = 'Failed to get response from Gemini API'
        resp['replica_count'] = -1
        return jsonify(resp), 500
    response = response.get('text')
    replica_count = response.replace("\n", "")
    resp['status'] = 'success'
    resp['message'] = 'Response from Gemini API'
    resp['replica_count'] = int(replica_count)
    print(resp)
    return jsonify(resp), 200

if __name__ == '__main__':
    app.run(debug=True) 