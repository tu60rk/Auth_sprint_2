# run test | locust -f locust_tests.py --host=http://127.0.0.1:8000

import random

from faker import Faker
from locust import HttpUser, task

class UserBehavior(HttpUser):
    faker = Faker()

    def on_start(self):
        self.client.get("/")

    @task(2)
    def search_films(self):
        query = random.choice([self.faker.word(), 'Star'])
        self.client.get(f"/api/v1/films/search?query={query}&page_number={random.randint(0, 5)}&page_size={random.randint(1, 50)}")


    @task(1)
    def search_persons(self):
        query = random.choice([self.faker.word(), 'Ann', 'Ben'])
        self.client.get(f"/api/v1/persons/search?query={query}&page_number={random.randint(0, 5)}&page_size={random.randint(1, 50)}")