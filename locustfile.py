from locust import HttpUser, TaskSet, task, between
import random


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.register()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def register(self):
        self.client.post("/register",
                         {"name": "Locust", "password": "buzz", "email": f"{random.randint(1, 100000)}@beemail.com",
                          "address": "The Hive"})

    def logout(self):
        self.client.get("/logout")

    @task(1)
    def home(self):
        self.client.get("/")

    @task(1)
    def profile(self):
        self.client.get("/user")

    @task(1)
    def order(self):
        self.client.get("/order")

    @task(1)
    def place_order(self):
        self.client.post("/order", {"type": "Box1"})

    @task(1)
    def edit_order(self):
        self.client.post("/order", {"id": f"{random.randint(1, 100)}"})
        self.client.post("/order", {"new_type": "Box2"})



class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
