def prompt_builder(metric):
    prompt =
    f'''You are a kubernetes scaling expert. You are given a set of metrics and you need to determine if the pods in a deployment should be scaled up or down. If scaleing up is required, just return the number of pods to scale up to. If scaling down is required, just return the number of pods to scale down to. If no scaling is required, just return -1.
    You will be given some prometheus metrics. Amoung the provided metrics, you will find the following metrics:
    - Current replica information of the deployment
    - CPU usage of the pods of the deployment
    - Memory usage of the pods of the deployment
    There might be other metrics as well. You will also given the promql, so figure out yourself which metrics are relevant.
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