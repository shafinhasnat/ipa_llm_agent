from google import genai
# from google.genai import types

class LLM:
    def __init__(self, api_key, model):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        
    def ask(self, prompt):
        try:
            response = self.client.models.generate_content(model=self.model, contents=prompt)
            return {"status": "success", "text": response.text}
        except Exception as e:
            print(e)
            return {"status": "error", "text": None}
class Prompt:
    def __init__(self, metrics):
        self.metrics = metrics
    def prompt_builder(self):
        prompt = f'''You are a kubernetes scaling expert. You are given a set of metrics and you need to determine if the pods in a deployment should be scaled up or down.
        Based on your determination, you will just return the number of pods to scale up to or down to, nothing else.
        Remember, my target is not to compromise performance.
        You will be given some prometheus metrics. Among the provided metrics, you will find the following metrics:
        - Current replica information of the deployment
        - CPU usage of the pods of the deployment
        - Memory usage of the pods of the deployment
        You might also given resource and limits of the pods of the deployment.
        There might be other metrics as well. You will also given the promql, so figure out yourself which metrics are relevant.
        In this metrics, you will find timestamp and value of the metrics. Timestamp is in unix time. Focus on the change of the metrics value over time.
        Here are the promql and their corresponding metrics-
        {self.metrics}
        '''
        print(prompt)
        return prompt