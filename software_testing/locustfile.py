from locust import HttpUser, TaskSet, task, between, events, runners
import random

# Set your target host for testing
HOST_URL = "https://jsonplaceholder.typicode.com"
NUM_USERS = 120          # Number of users for the test
SPAWN_RATE = 5          # Spawn rate (users per second)

class JsonPlaceholderTests(TaskSet):
    @task
    def load_homepage(self):
        """Load the homepage to check basic availability."""
        self.client.get("/", name="Load Homepage")

    @task
    def get_posts(self):
        """Fetch a list of posts."""
        self.client.get("/posts", name="Get Posts")

    @task
    def get_single_post(self):
        """Fetch a single post by random ID."""
        post_id = random.randint(1, 100)
        self.client.get(f"/posts/{post_id}", name="Get Single Post")

    @task
    def create_post(self):
        """Simulate creating a post."""
        data = {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        self.client.post("/posts", json=data, name="Create Post")

    @task
    def concurrent_load_test(self):
        """Concurrent Load Test to simulate users hitting the server at the same time."""
        self.client.get("/posts", name="Concurrent User Test - Get Posts")
        post_id = random.randint(1, 100)
        self.client.get(f"/posts/{post_id}", name="Concurrent User Test - Get Single Post")
        self.client.post("/posts", json={"title": "concurrent", "body": "test", "userId": 1}, name="Concurrent User Test - Create Post")

class WebsiteUser(HttpUser):
    tasks = [JsonPlaceholderTests]
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
