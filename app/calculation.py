def add(a:int, b:int):
    return a+b


class BankAccount():
    def __init__(self,starting_balence=0):
        self.balence = starting_balence

    def deposite(self, amount):
        self.balence += amount

    def withdraw(self, amount):
        self.balence -= amount

    def collect_intrest(self):
        self.balence *= 1.1
