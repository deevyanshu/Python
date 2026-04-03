class Dog:
    def __init__(self,name,breed, owner):
        self.name=name
        self.breed=breed
        self.owner=owner

    def bark(self):
        print("Whoof whoof")

class Owner:
    def __init__(self,name, address, contact_number):
        self.name=name
        self.address=address
        self.contact_number=contact_number

owner1=Owner("John Doe","123 Main St","555-1234")
dog1=Dog("Bruce","labraador",owner1)
print(dog1.name)
print(dog1.breed)
print(dog1.owner.name)
dog1.bark()