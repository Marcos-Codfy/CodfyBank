# CodfyBank - Simulação de Internet Banking em Python

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Bem-vindo ao CodfyBank! Este projeto é uma simulação de um sistema de internet banking desenvolvido inteiramente em Python. Ele foi criado como um exercício prático para aplicar conceitos de lógica de programação, orientação a objetos e regras de negócio em um ambiente que simula uma aplicação real.

## Funcionalidades

O sistema oferece um fluxo completo para o cliente bancário, incluindo:

* **Autenticação Segura**: Login com agência, conta e senha.
* **Gestão de Conta**: Visualização de saldo e dados do cliente.
* **Operações Financeiras**:
    * Depósito
    * Saque
    * Extrato de transações
* **Módulo PIX**:
    * Cadastro e consulta de chaves (CPF, CNPJ, E-mail, Telefone) com validação de formato.
    * Transferências para outras chaves e para si mesmo.
* **Configurações**:
    * Alteração de senha.
    * Ajuste manual do limite de crédito disponível.

## Regras de Negócio

Uma das principais características do projeto é a lógica de **limite de crédito dinâmico**:

1.  **Aumento Automático**: O limite máximo do cliente aumenta automaticamente toda vez que um depósito de valor recorde é realizado. O aumento é cumulativo e corresponde ao dobro do valor depositado.
2.  **Ajuste Manual**: O cliente tem controle sobre seu limite disponível, podendo ajustá-lo manualmente a qualquer momento, desde que não ultrapasse o teto aprovado pelo sistema e não seja inferior ao valor que ele já está utilizando. Essa lógica dupla, que combina um aumento automático com um ajuste manual, simula de forma realista como os bancos trabalham para fidelizar bons clientes.

## Como Executar o Projeto

Para rodar o CodfyBank, você precisa ter o Python instalado em sua máquina.

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
    ```
2.  Navegue até a pasta do projeto:
    ```bash
    cd CodfyBank-f8e2b4f61a15578185dddb3db9694a4710713a5c/CodfyBank
    ```
3.  Execute o arquivo principal:
    ```bash
    python CodfyBank.py
    ```

---

### **Como se Autenticar na Aplicação**

O projeto já vem com um usuário pré-cadastrado para facilitar os testes. Para fazer o login, utilize os seguintes dados quando solicitado na tela inicial:

* **Agência**: `0001`
* **Conta**: `15935-7`
* **Senha**: `010120`

A senha digitada não aparecerá na tela por questões de segurança.

---

## Tecnologias Utilizadas

* **Linguagem**: Python 3
* **Ambiente de Desenvolvimento**: Visual Studio Code Community
* **Módulos Nativos**: `os`, `getpass`, `time.sleep`
* **Conceitos Aplicados**:
    * Programação Orientada a Objetos (POO)
    * Estrutura de Dados
    * Manipulação de Entradas do Usuário
    * Lógica Condicional e de Negócios

## Autor

**Marcos Vinicius**

* [LinkedIn](https://www.linkedin.com/in/seu_perfil_linkedin) * [GitHub](https://github.com/marcos-codfy) ````
