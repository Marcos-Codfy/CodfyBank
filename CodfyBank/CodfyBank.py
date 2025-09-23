import os 
import getpass
from time import sleep 
import Customer 

# VARIÁVEIS GLOBAIS 
valid_login = False 
user = Customer.Customer() 

# FUNÇÕES 
def clear_screen(): 
    os.system("cls" if os.name == "nt" else "clear") 


def register_pix_key(resposta): 
    """Registra uma nova chave Pix com validação de CPF, Telefone, CNPJ ou E-mail.""" 
    if resposta != "sim": 
        print("Operação cancelada.") 
        sleep(2) 
        return 

    while True: 
        clear_screen() 
        print("Cadastro de Chave PIX") 
        print("=======================") 
        print("Tipos disponíveis:") 
        print("1 – CPF") 
        print("2 – Telefone") 
        print("3 – CNPJ") 
        print("4 – E-mail") 
        tipo_input = input("Escolha o tipo de chave (1|2|3|4): ").strip() 

        if tipo_input == "1": 
            tipo = "cpf" 
        elif tipo_input == "2": 
            tipo = "telefone" 
        elif tipo_input == "3": 
            tipo = "cnpj" 
        elif tipo_input == "4": 
            tipo = "email" 
        else: 
            print("\nOpção de tipo inválida. Tente novamente.") 
            sleep(2) 
            continue 

        chave = input(f"\nDigite sua chave ({tipo}): ").strip() 

        # Normalizar e validar 
        if tipo in ("cpf", "telefone", "cnpj"): 
            digitos = "".join(filter(str.isdigit, chave)) 
            tamanho = len(digitos) 
            if ( 
                (tipo == "cpf" and tamanho != 11) 
                or (tipo == "telefone" and tamanho not in (10, 11)) 
                or (tipo == "cnpj" and tamanho != 14) 
            ): 
                print("\nChave PIX inválida. Tente novamente.") 
                sleep(2) 
                continue 
            chave_valida = digitos 
        else:  # email 
            if "@" not in chave or "." not in chave.split("@")[-1]: 
                print("\nChave PIX inválida. Tente novamente.") 
                sleep(2) 
                continue 
            chave_valida = chave.lower() 

        # tudo ok: cadastra e confirma 
        user.add_pix_key(tipo, chave_valida) 
        print("\nChave PIX cadastrada com sucesso!") 
        sleep(2) 
        Pix() 
        break 


def Pix(): 
    clear_screen() 
    print("Área PIX") 
    print("=======================") 

    if not user.pix_keys: 
        print("Sem chave PIX cadastrada.") 
        print("\nDeseja cadastrar agora?") 
        resposta = input("Digite 'sim' para cadastrar: ").strip().lower() 
        register_pix_key(resposta) 
    else: 
        print("Chaves PIX cadastradas:") 
        for p in user.pix_keys: 
            print(f"- {p['tipo'].upper()}: {p['chave']}") 
        print("=======================") 
        print("\n1 – Cadastrar nova chave") 
        print("2 – Voltar ao menu") 
        escolha = input("Opção: ").strip() 
        if escolha == "1": 
            register_pix_key("sim") 

def TransferenciaPix():
    clear_screen()
    print("Área de Transferência - PIX")
    print("=======================")
    pix_destino = input("Digite a chave PIX do destinatário: ").strip()
    valor = input("Digite o valor a ser transferido: R$ ").strip().replace(',', '.')
    # Validação simples para ver se é um número
    if not valor.replace('.', '', 1).isdigit():
        print("\nValor inválido. Por favor, digite um número.")
        sleep(2)
        input("\nPressione Enter para voltar ao menu...")
        return

    valor_float = float(valor)
    if valor_float <= 0:
        print("\nO valor da transferência deve ser positivo.")
        sleep(2)
        input("\nPressione Enter para voltar ao menu...")
        return

    # Lógica para verificar se a transferência é para si mesmo
    chaves_do_usuario = []
    for chave in user.pix_keys:
        chaves_do_usuario.append(chave['chave'])

    # Se a chave de destino está na lista de chaves do usuário
    if pix_destino in chaves_do_usuario:
        print(f"\nTransferindo R$ {valor_float:.2f} para você mesmo...")
        sleep(2)
        # Apenas registra no extrato, sem alterar o saldo
        user.registrar_extrato(f"Transferência PIX para si mesmo de R$ {valor_float:.2f}")
        print("Operação realizada com sucesso!")
    
    # Se for para outra pessoa, usa a lógica de débito normal
    else:
        print(f"\nTransferindo R$ {valor_float:.2f} para a chave PIX {pix_destino}...")
        sleep(2)
        if user.debito(valor_float):
            print("Transferência realizada com sucesso!")
            user.registrar_extrato(f"Transferência PIX de R$ {valor_float:.2f} para {pix_destino}")
        else:
            print("Saldo e limite insuficientes para a transferência.")
            sleep(2)
            
    input("\nPressione Enter para voltar ao menu...")


def TransferenciaAgenciaConta(): 
    clear_screen() 
    print("Área de Transferência - Agência e Conta") 
    print("=======================") 
    agencia_destino = input("Digite a agência do destinatário: ").strip() 
    conta_destino = input("Digite a conta do destinatário: ").strip() 
    valor = input("Digite o valor a ser transferido: R$ ").strip() 
    valor_float = float(valor)
    print(f"\nTransferindo R$ {valor} para a conta {conta_destino} da agência {agencia_destino}...") 
    sleep(2) 
    if user.debito(valor_float):
        print("Transferência realizada com sucesso!") 
        user.registrar_extrato(f"Transferência de R$ {valor_float:.2f} para {agencia_destino}/{conta_destino}")
    else:
        print("Saldo e limite insuficientes para a transferência.")
        sleep(2)
    input("\nPressione Enter para voltar ao menu...")


def Deposito(): 
    clear_screen() 
    print("Área de Depósito") 
    print("=======================") 
    valor = input("Digite o valor a ser depositado: R$ ").strip()
    print(f"\nDepositando R$ {valor} na sua conta...")
    sleep(2)
    print("Depósito realizado com sucesso!")
    user.credito(float(valor))  # Só esta linha já atualiza saldo e limite corretamente
    user.registrar_extrato(f"Depósito de R$ {float(valor):.2f}")
    input("\nPressione Enter para voltar ao menu...") 


def Saque(): 
    clear_screen() 
    print("Área de Saque") 
    print("=======================") 
    valor = input("Digite o valor a ser sacado: R$ ").strip() 
    valor_float = float(valor)
    if user.debito(valor_float):
        print(f"\nSacando R$ {valor} da sua conta...") 
        sleep(2) 
        print("Saque realizado com sucesso!") 
        user.registrar_extrato(f"Saque de R$ {valor_float:.2f}")
    else:
        print("\nSaldo e limite insuficientes para o saque.") 
        sleep(2)
    input("\nPressione Enter para voltar ao menu...")

def AjustarLimite():
    clear_screen()
    print("Ajuste de Limite Disponível")
    print("===========================")
    
    valor_utilizado = user.limite_maximo - user.limit
    
    print(f"Seu limite máximo aprovado é: R$ {user.limite_maximo:.2f}")
    print(f"Seu limite disponível atual é: R$ {user.limit:.2f}")
    if valor_utilizado > 0:
        print(f"Você já está utilizando R$ {valor_utilizado:.2f} do seu limite.")
    
    print("\nVocê pode ajustar seu limite disponível.")
    print(f"O valor deve estar entre R$ {valor_utilizado:.2f} e R$ {user.limite_maximo:.2f}.")
    
    valor_str = input("Digite o novo valor para o limite disponível: R$ ").strip().replace(',', '.')
    
    # Validação simples para ver se é um número
    if not valor_str.replace('.', '', 1).isdigit():
        print("\nEntrada inválida. Por favor, digite um número.")
    else:
        novo_limite = float(valor_str)
        # Chama o método da classe que contém a lógica
        mensagem = user.ajustar_limite(novo_limite)
        print(f"\n{mensagem}")

    sleep(3)
    input("\nPressione Enter para voltar ao menu...")


def Extrato(): 
    clear_screen() 
    print("Extrato da Conta") 
    print("=======================") 
    print(f"Cliente: {user.name} {user.last_name}") 
    print(f"Agência: {user.agency}  Conta: {user.account}") 
    print(f"Saldo Atual: R$ {user.balance:.2f}") 
    print("=======================") 
    print("Operações:")
    if not user.extrato:
        print("Nenhuma operação realizada.")
    else:
        for operacao in user.extrato:
            print(f"- {operacao}")
    input("\nPressione Enter para voltar ao menu...") 

# FUNÇÃO CONFIGURACOES ATUALIZADA

def Configuracoes():
    clear_screen()
    print("Área de Configurações")
    print("=======================")
    print(f"Nome: {user.name} {user.last_name}")
    print(f"Agência: {user.agency}  Conta: {user.account}")
    print("----------------------")
    print("1 - Alterar Nome")
    print("2 - Alterar Senha")
    print("3 - Ajustar Limite")
    print("0 - Voltar ao Menu")
    escolha = input("Opção: ").strip()

    if escolha == "1":
        novo_nome = input("Digite o novo nome: ").strip()
        novo_sobrenome = input("Digite o novo sobrenome: ").strip()
        user.name = novo_nome
        user.last_name = novo_sobrenome
        print("Nome alterado com sucesso!...")
        sleep(2)
    elif escolha == "2":
        print("Para alterar a senha, informe a senha atual.")
        senha_atual = input("Senha atual: ").strip()
        if senha_atual == user.password:
            nova_senha = input("Digite a nova senha: ").strip()
            confirmar_senha = input("Confirme a nova senha: ").strip()
            if nova_senha == confirmar_senha:
                user.password = nova_senha
                print("Senha alterada com sucesso!...")
            else:
                print("As senhas não coincidem. Tente novamente.")
        else:
            print("Senha atual incorreta.")
        sleep(2)
    elif escolha == "3":
        AjustarLimite()


def Home(): 
    clear_screen() 
    print("Bem vindo ao Codfy Bank") 
    print("=======================") 
    print(f"Cliente: {user.name} {user.last_name}") 
    print(f"Agência: {user.agency}  Conta: {user.account}") 
    print(f"Saldo: R$ {user.balance:.2f} - Limite: {user.limit}") 
    print("____________") 
    print("1 – Deposito") 
    print("2 – Saque") 
    print("3 – Extrato") 
    print("4 – PIX") 
    print("5 - Transferência - PIX") 
    print("6 - Transferência - Agência e Conta") 
    print("7 - Configurações")
    print("0 – Sair") 
    print("____________") 

    option_menu = input("Selecione a Opção desejada: ").strip() 
    if option_menu == "1":
        Deposito()
    elif option_menu == "2":
        Saque()
    elif option_menu == "3":
        Extrato()
    elif option_menu == "4":
        Pix()
    elif option_menu == "5":
        TransferenciaPix()
    elif option_menu == "6":
        TransferenciaAgenciaConta()
    elif option_menu == "7":
        Configuracoes()
    elif option_menu == "0":
        print("\nSaindo...")
        sleep(1)
        exit()
    else:
        print("\nOpção ainda não implementada.")
        sleep(1.5)

# 5. EXECUÇÃO PRINCIPAL DO PROGRAMA 
# Login 
while not valid_login: 
    clear_screen() 
    print("Bem vindo ao Codfy Bank") 
    print("=======================") 
    input_agency = input("Digite sua agência: ").strip() 
    input_account = input("Digite sua conta: ").strip() 
    # Aqui a senha não aparece na tela
    input_password = getpass.getpass("Digite sua senha: ").strip()  

    if (input_agency == user.agency and 
        input_account == user.account and 
        input_password == user.password): 
        print("\nLogin realizado com sucesso!") 
        valid_login = True 
        sleep(1.5) 
    else: 
        print("\nDados incorretos!") 
        sleep(1.5)

# Loop principal 
while True: 
    Home()

