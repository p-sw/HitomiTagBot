def one_of(callback):
    def test_inner(**kwargs):
        print("1 inner in")
        print(str(kwargs))
        print("1 inner out")
        return callback()
    return test_inner

class two_of(object):
    def __init__(self, **kwargs):
        self.args = kwargs
    def __call__(self, func):
        def wrapper():
            return func(**self.args)
        return wrapper

@two_of(hello="world")
@one_of
def hello():
    print("Hello!")


hello()