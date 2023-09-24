from locust import HttpUser, task, between, TaskSet

class BlogUser(HttpUser):
    wait_time = between(2, 5) 

    
    @task(1)
    def view_homepage(self):
        self.client.get("/")

    @task(2)
    def view_post(self):
        self.client.get(f"/article/3")

    @task(3)
    def add_post(self):
        self.client.get("/add_post/")

    @task(4)
    def edit_post(self):
        self.client.get(f"/article/edit/3")

    @task(5)
    def delete_post(self):
        self.client.get(f"/article/3/remove")

