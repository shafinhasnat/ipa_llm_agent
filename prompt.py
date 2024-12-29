def prompt_builder(metrics):
    prompt = f'''You are a kubernetes scaling expert. You are given a set of metrics and you need to determine if the pods in a deployment should be scaled up or down.
    Based on your determination, you will just return the number of pods to scale up to or down to, nothing else.
    Remember, my target is to save money but not compromise performance.
    You will be given some prometheus metrics. Among the provided metrics, you will find the following metrics:
    - Current replica information of the deployment
    - CPU usage of the pods of the deployment
    - Memory usage of the pods of the deployment
    There might be other metrics as well. You will also given the promql, so figure out yourself which metrics are relevant.
    In this metrics, you will find timestamp and value of the metrics.
    Here are the promql and their corresponding metrics-
    {metrics}
    '''
    return prompt

def gemini_prompt(metrics):
    return {
        "contents": [{
            "parts": [{"text": prompt_builder(metrics)}]
        }]
    }