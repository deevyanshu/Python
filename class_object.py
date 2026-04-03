class Car:
    total_car=0
    def __init__(self,brand,model):
        self.__brand=brand
        self.__model=model
        self.total_car+=1
    
    def get_brand(self):
        return self.__brand
    
    @property
    def get_model(self):
        return self.__model
    
    def set_brand(self,brand):
        self.__brand=brand
    
    # def set_model(self,model):
    #     self.__model=model
    
    
    def fullname(self):
        return f"{self.__brand} {self.__model}"
    
    @staticmethod
    def description():
        return "cars are means of transport"

class ElectricCar(Car):
    def __init__(self,brand,model,battery_size):
        super().__init__(brand,model)
        self.__battery_size=battery_size
    
    def get_battery_size(self):
        return self.__battery_size
    
    def set_battery_size(self,battery_size):
        self.__battery_size=battery_size
    
    def battery_info(self):
        return f"{self.get_brand()} {self.get_model} has a {self.__battery_size} kWh battery."



#object
my_car=Car("toyota","corolla")
# print(my_car.fullname())
# print(my_car.get_brand())
# print(my_car.get_model)

electric_car=ElectricCar("tesla","model 3",75)
print(electric_car.battery_info())