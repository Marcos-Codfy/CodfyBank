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
    def __init__(self):
        self.pix_Keys = []







         