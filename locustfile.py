from locust import HttpUser, task, between

class PrimeUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def small_prime(self):
        self.client.get("/primes?n=10")

    @task
    def medium_prime(self):
        self.client.get("/primes?n=50")

    @task
    def async_prime(self):
        res = self.client.post("/primes/async?n=10")
        if res.status_code == 200:
            task_id = res.json().get("task_id")
            self.client.get(f"/tasks/{task_id}")
