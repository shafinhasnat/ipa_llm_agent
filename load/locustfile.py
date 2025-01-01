from locust import HttpUser, task, between

class MyUser(HttpUser):
    host = "http://localhost:8001"
    wait_time = between(0, 0)  # No wait time between requests for maximum concurrency
    
    @task
    def test_endpoint(self):
        self.client.get("/1000") 