class Customer:
    def __init__(self, name = None,
                 last_name = None,
                 agency = None,
                 account = None,
                 password = None,
                 balance = None,
                 statement = None,
                 limit = None):
        self.name = "Silvano"
        self.last_name = "Malfatti"
        self.agency = "0001"
        self.account = "15935-7"
        self.password = "010120"
        self.balance = 0.0
        self.pix_keys = []
        self.statement = []
        self.limit = 0.0
        self.maximum_limit = 0.0
        self.largest_deposit_made = 0.0

    def add_pix_key(self, key_type, key_value):
        self.pix_keys.append({'type': key_type, 'key': key_value})

    def register_statement(self, operation):
        self.statement.append(operation)

    def debit(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        elif amount <= (self.balance + self.limit):
            amount_used_from_limit = amount - self.balance
            self.balance = 0.0
            self.limit -= amount_used_from_limit
            return True
        else:
            return False

    def credit(self, amount):
        # Part 1: The money enters the account (replenishing the limit first)
        if self.limit < self.maximum_limit:
            amount_to_replenish = self.maximum_limit - self.limit
            if amount >= amount_to_replenish:
                # If the deposit covers the used limit, the available limit returns to the maximum
                self.limit = self.maximum_limit
                self.balance += (amount - amount_to_replenish)
            else:
                self.limit += amount
        else:
            self.balance += amount

        # Part 2: The limit increase rule
        if amount > self.largest_deposit_made:
            self.largest_deposit_made = amount
            
            # Calculates only the INCREASE amount
            limit_increase = amount * 2
            
            # Adds the increase to the maximum limit (ceiling)
            self.maximum_limit = self.maximum_limit + limit_increase
            
            # Adds the same increase to the user's available limit
            self.limit = self.limit + limit_increase

    def adjust_limit(self, new_value):
        used_amount = self.maximum_limit - self.limit

        if new_value > self.maximum_limit:
            return f"Invalid value. The limit cannot be greater than the maximum approved of R$ {self.maximum_limit:.2f}."
        
        if new_value < used_amount:
            return f"Invalid value. You have already used R$ {used_amount:.2f}. The limit cannot be less than this."

        self.limit = new_value
        return f"Limit successfully adjusted to R$ {self.limit:.2f}."

class Pix():
    def __init__(self):
        self.pix_keys = []
