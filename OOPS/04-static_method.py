class BankBalance:
    MIN_BALANCE=100

    def __init__(self,owner,balance=0):
        self.owner=owner
        self.balance=balance
    
    def deposit(self,amount):
        if self._is_valid_amount(amount):
            self.balance+=amount
            self.__log_transaction("Deposit",amount)
        else:
            print("Deposit amount must be positive.")
    
    def _is_valid_amount(self,amount): # Protected method to validate amount
        return amount>0
    
    def __log_transaction(self,transaction_type,amount): # Private method to log transactions
        print(f"{transaction_type} of ${amount} for {self.owner}. Current balance: ${self.balance}")
    
    @staticmethod
    def is_valid_interest_rate(rate):
        return 0<=rate<=5

account=BankBalance("Alice",500)
account.deposit(200)
print(BankBalance.is_valid_interest_rate(3))