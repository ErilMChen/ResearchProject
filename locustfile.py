import locust
import json
from locust import HttpLocust, TaskSet, between


class WebsiteUser(locust.HttpUser):
    @locust.task
    def login(self):
        response = self.client.get('')
        csrftoken = response.cookies['csrftoken']
        self.client.post("login/", {"username": "hi@email.com", "password": "dublinbus"}, headers={"X-CSRFToken": csrftoken})
        self.client.get('mystations')

    @locust.task
    def logout(self):
        response = self.client.get('')
        csrftoken = response.cookies['csrftoken']
        self.client.post("logout/", {"username": "hi@email.com", "password": "dublinbus"}, headers={"X-CSRFToken": csrftoken})
