class Customer:
    def __init__(self, name = None,
                 last_name = None,
                 agency = None,
                 account = None,
                 password = None,
                 balance = None,
                 extrato = None,
                 limit = None):
        self.name = "Silvano"
        self.last_name = "Malfatti"
        self.agency = "0001"
        self.account = "15935-7"
        self.password = "010120"
        self.balance = 0.0
        self.pix_keys = []
        self.extrato = []
        self.limit = 0.0
        self.limite_maximo = 0.0
        self.maior_deposito_realizado = 0.0

    def add_pix_key(self, tipo, chave):
        self.pix_keys.append({'tipo': tipo, 'chave': chave})

    def registrar_extrato(self, operacao):
        self.extrato.append(operacao)

    def debito(self, valor):
        if valor <= self.balance:
            self.balance -= valor
            return True
        elif valor <= (self.balance + self.limit):
            valor_usado_limite = valor - self.balance
            self.balance = 0.0
            self.limit -= valor_usado_limite
            return True
        else:
            return False

    def credito(self, valor):
        # Parte 1: O dinheiro entra na conta (repondo o limite primeiro)
        if self.limit < self.limite_maximo:
            falta_repor = self.limite_maximo - self.limit
            if valor >= falta_repor:
                # Se o depósito cobre o limite usado, o limite disponível volta ao máximo
                self.limit = self.limite_maximo
                self.balance += (valor - falta_repor)
            else:
                self.limit += valor
        else:
            self.balance += valor

        # Parte 2: A regra de aumento do limite
        if valor > self.maior_deposito_realizado:
            self.maior_deposito_realizado = valor
            
            # Calcula apenas o valor do AUMENTO
            aumento_de_limite = valor * 2
            
            # Soma o aumento ao limite máximo (teto)
            self.limite_maximo = self.limite_maximo + aumento_de_limite
            
            # Soma o mesmo aumento ao limite disponível do usuário
            self.limit = self.limit + aumento_de_limite

    def ajustar_limite(self, novo_valor):
        valor_utilizado = self.limite_maximo - self.limit

        if novo_valor > self.limite_maximo:
            return f"Valor inválido. O limite não pode ser maior que o máximo aprovado de R$ {self.limite_maximo:.2f}."
        
        if novo_valor < valor_utilizado:
            return f"Valor inválido. Você já utilizou R$ {valor_utilizado:.2f}. O limite não pode ser menor que isso."

        self.limit = novo_valor
        return f"Limite ajustado com sucesso para R$ {self.limit:.2f}."

class Pix():
    def __init__(self):class Customer:
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
        self.pix_Keys = []







         
