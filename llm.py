import json
from google import genai
# from google.genai import types

class LLM:
    def __init__(self, api_key, model):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        
    def ask(self, prompt):
        try:
            response = self.client.models.generate_content(model=self.model, contents=prompt)
            response_text = response.text
            print("---- GEMINI RESPONSE ----\n",response_text,"\n---- ----")
            response_text = response_text.split("```json")[1].split("```")[0].strip()
            return {"status": "success", "text": json.loads(response_text)}
            # return {"status": "success", "text": {'replicas': 2, 'cpu_limit': '500m', 'memory_limit': '150Mi', 'cpu_request': '200m', 'memory_request': '64Mi'}}
        except Exception as e:
            print(e)
            return {"status": "error", "text": None}
        
class Prompt:
    def __init__(self, metrics):
        self.metrics = metrics
    def prompt_builder(self):
        prompt = f'''You are given a set of metrics for a Kubernetes deployment, including the current replica count, CPU usage per pod, memory usage per pod, and node available memory. Your task is to determine the optimal number of replicas and resource requests/limits to ensure the deployment operates efficiently without running out of resources or being OOM-killed. The goal is to maximize resource efficiency while ensuring stability, scalability, and resilience to workload spikes.

Steps to Follow:
Analyze Resource Usage:

Evaluate the average, peak, and spike CPU and memory usage of all existing pods over a suitable time range.
If available, consider the 90th or 95th percentile usage to account for transient spikes.
Check if the current resource requests and limits for CPU and memory are appropriate based on both observed utilization and expected workload variability.
Adjust Resource Requests and Limits Conservatively:

Memory Requests and Limits:
Set memory requests based on the peak observed usage with an additional safety margin (e.g., +20%-50%).
Set memory limits to at least 2x the request to allow flexibility for spikes.
Ensure the memory request is not too low (e.g., minimum 50Mi) and does not exceed node capacity.
CPU Requests and Limits:
Set CPU requests based on the average observed usage with a safety margin.
Set CPU limits to at least 2x the request to accommodate workload spikes.
Avoid setting CPU requests and limits too low, which can lead to throttling and degraded performance.
Determine Replica Count:

Ensure the combined workload can be handled by the specified number of replicas without over-utilizing resources.
Reduce replicas only if the remaining pods can handle the workload within the adjusted resource limits.
Add replicas if necessary to distribute the workload, ensuring no single pod exceeds 80% of its allocated resources under peak usage.
Account for Node Resource Availability:

Ensure the combined resource requests of all pods (including replicas) do not exceed the node's available resources.
Leave room for other workloads and Kubernetes system components.
Output Format:
Return the following configuration in JSON format:

"replicas": <minimum number of replicas required (positive integer)>,
"cpu_limit": <CPU limit per pod (string, in millicores, e.g., "100m")>,
"memory_limit": <Memory limit per pod (string, in Mebibytes, e.g., "100Mi")>,
"cpu_request": <CPU request per pod (string, in millicores, e.g., "50m")>,
"memory_request": <Memory request per pod (string, in Mebibytes, e.g., "50Mi")>

Notes:
Prioritize horizontal scaling over vertical scaling to ensure optimal growth and flexibility.
Avoid reducing resource requests and limits excessively to prevent under-provisioning.
Add a buffer margin for resource requests and limits to handle unexpected spikes and workload variability.
If the application still fails, consider reviewing its code for memory or CPU-intensive operations, or assess whether the workload is appropriate for a Kubernetes deployment.
This prompt ensures that resource requests and limits are configured with safety margins, significantly reducing the likelihood of OOM kills or resource throttling while maintaining efficient resource utilization.

Metrics-


{self.metrics}
        '''
        print(prompt)
        return prompt
    

# if __name__ == "__main__":
#     metrics = """
# Deployment replicas - promql: kube_deployment_spec_replicas{deployment="cpuload", namespace="cpuload"} metrics: {"status":"success","data":{"resultType":"matrix","result":[{"metric":{"__name__":"kube_deployment_spec_replicas","app_kubernetes_io_component":"metrics","app_kubernetes_io_instance":"prometheus","app_kubernetes_io_managed_by":"Helm","app_kubernetes_io_name":"kube-state-metrics","app_kubernetes_io_part_of":"kube-state-metrics","app_kubernetes_io_version":"2.14.0","deployment":"cpuload","helm_sh_chart":"kube-state-metrics-5.27.0","instance":"10.244.0.135:8080","job":"kubernetes-service-endpoints","namespace":"cpuload","node":"minikube","service":"prometheus-kube-state-metrics"},"values":[[1735644842,"3"],[1735644902,"3"],[1735644962,"3"],[1735645022,"3"],[1735645082,"3"],[1735645142,"3"]]}]}}
# CPU usage - promql: rate(container_cpu_usage_seconds_total{pod=~"cpuload-fc45cf69c-lmvct|cpuload-78b8fc6699-cjlbk|cpuload-b8c87979d-xqtk5|cpuload-fc45cf69c-d6m2t", namespace="cpuload"}[2m]) metrics: {"status":"success","data":{"resultType":"matrix","result":[{"metric":{"beta_kubernetes_io_arch":"amd64","beta_kubernetes_io_os":"linux","cpu":"total","id":"/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod393abf72_4e40_457e_b9ea_9ccb589a54ad.slice","instance":"minikube","job":"kubernetes-nodes-cadvisor","kubernetes_io_arch":"amd64","kubernetes_io_hostname":"minikube","kubernetes_io_os":"linux","minikube_k8s_io_commit":"210b148df93a80eb872ecbeb7e35281b3c582c61","minikube_k8s_io_name":"minikube","minikube_k8s_io_primary":"true","minikube_k8s_io_updated_at":"2024_11_25T17_14_33_0700","minikube_k8s_io_version":"v1.34.0","namespace":"cpuload","pod":"cpuload-fc45cf69c-lmvct"},"values":[[1735644842,"0.00019466273261079106"],[1735644902,"0.0001807433266915867"],[1735644962,"0.00019074456410542596"],[1735645022,"0.00019101968967817986"],[1735645082,"0.0002028004788922999"],[1735645142,"0.00019597152535004658"]]},{"metric":{"beta_kubernetes_io_arch":"amd64","beta_kubernetes_io_os":"linux","cpu":"total","id":"/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod830feec7_0d94_4c91_a1b4_1fa4eeffabed.slice","instance":"minikube","job":"kubernetes-nodes-cadvisor","kubernetes_io_arch":"amd64","kubernetes_io_hostname":"minikube","kubernetes_io_os":"linux","minikube_k8s_io_commit":"210b148df93a80eb872ecbeb7e35281b3c582c61","minikube_k8s_io_name":"minikube","minikube_k8s_io_primary":"true","minikube_k8s_io_updated_at":"2024_11_25T17_14_33_0700","minikube_k8s_io_version":"v1.34.0","namespace":"cpuload","pod":"cpuload-b8c87979d-xqtk5"},"values":[[1735644842,"0.00018148680734374434"],[1735644902,"0.00019764290666162475"],[1735644962,"0.00018742753870285803"],[1735645022,"0.00019279433209114553"],[1735645082,"0.00020211131155208124"],[1735645142,"0.00021945999018164005"]]},{"metric":{"beta_kubernetes_io_arch":"amd64","beta_kubernetes_io_os":"linux","cpu":"total","id":"/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-poded717ea8_c4c6_48cc_a4cf_d01b962c08ed.slice","instance":"minikube","job":"kubernetes-nodes-cadvisor","kubernetes_io_arch":"amd64","kubernetes_io_hostname":"minikube","kubernetes_io_os":"linux","minikube_k8s_io_commit":"210b148df93a80eb872ecbeb7e35281b3c582c61","minikube_k8s_io_name":"minikube","minikube_k8s_io_primary":"true","minikube_k8s_io_updated_at":"2024_11_25T17_14_33_0700","minikube_k8s_io_version":"v1.34.0","namespace":"cpuload","pod":"cpuload-fc45cf69c-d6m2t"},"values":[[1735644842,"0.00018772917515463448"],[1735644902,"0.00018741586557496494"],[1735644962,"0.00018916891449731016"],[1735645022,"0.0001832509836215571"],[1735645082,"0.0001936856572704807"],[1735645142,"0.00020604907813706432"]]}]}}
# RAM usage - promql: avg(container_memory_usage_bytes{pod=~"cpuload-fc45cf69c-lmvct|cpuload-78b8fc6699-cjlbk|cpuload-b8c87979d-xqtk5|cpuload-fc45cf69c-d6m2t", namespace="cpuload"}) metrics: {"status":"success","data":{"resultType":"matrix","result":[{"metric":{},"values":[[1735644842,"20832256"],[1735644902,"20832256"],[1735644962,"20832256"],[1735645022,"20832256"],[1735645082,"20832256"],[1735645142,"20832256"]]}]}}
# Resource request and limits: CPU Resource Requests: 1, CPU Resource Limits: 2, Memory Resource Requests: 20000Mi, Memory Resource Limits: 27008Mi
# Node available memory - promql: node_memory_MemAvailable_bytes metrics: {"status":"success","data":{"resultType":"matrix","result":[{"metric":{"__name__":"node_memory_MemAvailable_bytes","app_kubernetes_io_component":"metrics","app_kubernetes_io_instance":"prometheus","app_kubernetes_io_managed_by":"Helm","app_kubernetes_io_name":"prometheus-node-exporter","app_kubernetes_io_part_of":"prometheus-node-exporter","app_kubernetes_io_version":"1.8.2","helm_sh_chart":"prometheus-node-exporter-4.42.0","instance":"192.168.49.2:9100","job":"kubernetes-service-endpoints","namespace":"default","node":"minikube","service":"prometheus-prometheus-node-exporter"},"values":[[1735644842,"27854655488"],[1735644902,"27844677632"],[1735644962,"27931721728"],[1735645022,"27969671168"],[1735645082,"27807936512"],[1735645142,"27842899968"]]}]}}
# """
#     prompt = Prompt(metrics)
#     prompt_text = prompt.prompt_builder()
#     llm = LLM("AIzaSyBPOFq3ux-m7M9qi0dzOZhssOb1xM3YTxY", "gemini-1.5-flash")
#     response = llm.ask(prompt_text)
#     print(response)