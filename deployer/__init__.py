class Deployer:
    def __init__(self, url):
        self.url = url
        self.environment = "production"

    def set_environment(self, environment):
        self.environment = environment

    def deploy(self):
        return "Not (yet) implemented"
