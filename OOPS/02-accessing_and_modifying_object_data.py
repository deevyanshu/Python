class User:
    def __init__(self, username, email, password):
        self.name = username
        self._email = email #protected
        self.__password = password #private
    
    def get_email(self):
        return self._email.lower().strip()
    
    def get_password(self):
        return self.__password
    
    def set_email(self,newEmail):
        self._email=newEmail

    def set_password(self,newPassword):
        self.__password=newPassword
    
    #alternative to getter and setter
    @property   
    def email(self):
        return self._email.lower().strip()
    
    @email.setter
    def email(self,newEmail):
        self._email=newEmail
    

user1=User("daman","daman@gmail.com","123")
print(user1.get_email())
# print(user1.__password) # this will give error, can only access through getter
print(user1.get_password())
print(user1.email)
user1.email="don@gmail.com"
print(user1.email)