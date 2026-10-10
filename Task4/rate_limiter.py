from locust import HttpUser, between, task


class WebUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_api(self):
        self.client.get(
            "/api/?client_type=web",
            headers={"client_type": "web"},
            name="GET /api/ web (50 r/s)",
        )


class MobileUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_api(self):
        self.client.get(
            "/api/?client_type=mobile",
            headers={"client_type": "mobile"},
            name="GET /api/ mobile (30 r/s)",
        )