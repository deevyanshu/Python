class User:
    user_count=0 #static attribute

    def __init__(self,username,email):
        self.username=username
        self.email=email
        User.user_count+=1
    
    def display_user(self):
        print(f"Username: {self.username}, Email: {self.email}")

user1=User("Don","don@gmail.com")
user2=User("Bob","bob@gmail.com")
print(User.user_count)
print(user1.user_count)
print(user2.user_count)