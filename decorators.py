import time 

def timer(func):
    def wrapper(*args, **kwargs):
        start=time.time()
        result=func(*args, **kwargs)
        end=time.time()
        print(f"{func.__name__} ran in {end-start} time")
        return result
    return wrapper

@timer
def example_function(n):
    time.sleep(n)

def debug(func):
    def wrapper(*args,**kwargs):
        args_value=', '.join(str(arg) for arg in args)
        print(f"calling: {func.__name__} with args {args_value}")
        return func(*args,**kwargs)
    return wrapper 

@debug
def greet(name,greeting="Hello"):
    print(f"{greeting}, {name}")

greet("chai", "namaste")    
example_function(2)