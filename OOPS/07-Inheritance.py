class Vehicle:
    def __init__(self, brand, model,year):
        self.brand = brand
        self.model = model
        self.year=year

    def start(self):
        print("vehicle is starting")
    
    def stop(self):
        print("vehicle is stopping")

class Car(Vehicle):
    def __init__(self, brand, model, year,doors,wheels):
        super().__init__(brand, model, year)
        self.doors=doors
        self.wheels=wheels
    

class Bike(Vehicle):
    def __init__(self, brand, model, year,wheels):
        super().__init__(brand, model, year)
        self.wheels=wheels

car=Car("Toyota", "Camry", 2020, 4, 4)
bike=Bike("Yamaha", "R15", 2021, 2)

print(car.__dict__)