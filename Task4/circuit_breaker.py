import os

from locust import HttpUser, between, task

ACTIVE = set(os.environ.get("SCENARIO", "broken,healthy").split(","))


class LoadOnBrokenBackend(HttpUser):
    abstract = "broken" not in ACTIVE
    wait_time = between(1, 3)

    @task
    def get_error(self):
        self.client.get("/logistics/?type=error", name="логистика: бэкенд отдаёт 500")


class LoadOnHealthyBackend(HttpUser):
    abstract = "healthy" not in ACTIVE
    weight = 3
    wait_time = between(1, 3)

    @task
    def get_fast(self):
        self.client.get("/logistics/?type=fast", name="логистика: бэкенд отвечает быстро")


class LoadOnTimedOutBackend(HttpUser):
    abstract = "timeout" not in ACTIVE
    weight = 2
    wait_time = between(1, 2)

    @task
    def get_slow(self):
        self.client.get("/logistics/?type=slow", name="логистика: бэкенд не отвечает дольше 3s")