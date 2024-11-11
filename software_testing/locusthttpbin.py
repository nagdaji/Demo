from locust import HttpUser, TaskSet, task, between, events, runners
import random

# Set the target host for testing
HOST_URL = "http://httpbin.org"
NUM_USERS = 10          # Number of users for the test
SPAWN_RATE = 5          # Spawn rate (users per second)

class HttpBinTests(TaskSet):
    @task
    def load_homepage(self):
        """Load the homepage to check basic availability."""
        self.client.get("/", name="Load Homepage")

    @task
    def get_request(self):
        """Perform a GET request to the /get endpoint."""
        self.client.get("/get", name="GET /get")

    @task
    def post_request(self):
        """Simulate a POST request to the /post endpoint."""
        data = {"name": "test", "value": random.randint(1, 100)}
        self.client.post("/post", json=data, name="POST /post")

    @task
    def concurrent_load_test(self):
        """Concurrent Load Test to simulate users hitting the server at the same time."""
        self.client.get("/get", name="Concurrent User Test - GET /get")
        self.client.post("/post", json={"name": "concurrent", "value": random.randint(1, 100)}, name="Concurrent User Test - POST /post")

class WebsiteUser(HttpUser):
    tasks = [HttpBinTests]
    wait_time = between(0.1, 0.5)  # Minimal wait time for concurrent access
    host = HOST_URL

# Automatically start the test with specified users and spawn rate
@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    if isinstance(environment.runner, runners.LocalRunner):
        environment.runner.start(NUM_USERS, spawn_rate=SPAWN_RATE)

# Automatically stop the test after a set duration (optional)
@events.quitting.add_listener
def on_quitting(environment, **_kwargs):
    print("Load test completed.")





# command for the csv file report creation
# locust -f locust_test_httpbin.py --csv=locust_results --host=http://httpbin.org
