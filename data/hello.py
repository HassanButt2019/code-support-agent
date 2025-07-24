def greet(name):
    return f"Hello, {name}!"

class Greeter:
    def __init__(self, name):
        self.name = name

    def say_hi(self):
        return greet(self.name)
