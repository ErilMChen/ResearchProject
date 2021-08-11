import locust

class HelloWorldUser(locust.HttpUser):
    @locust.task
    def hello_world(self):
        self.client.get("map")
        #self.client.get("/world")