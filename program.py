menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=>
"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0;
LIMITE_SAQUES = 3

while True:

    opcao = input(menu).lower()

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Operação falhou! O valor informado é inválido")
    
    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        msg = "Operação falhou! "
        valorPositivo = valor > 0
        possuiSaldo = valor <= saldo
        possuiLimite = valor <= limite
        possuiSaques = numero_saques < LIMITE_SAQUES

        if valorPositivo and possuiSaldo and possuiLimite and possuiSaques:
            saldo -= valor
            numero_saques += 1
            extrato += f"Saque: R$ {valor:.2f}\n"
        
        else:
            if not valorPositivo:
                msg += "O valor do saque deve ser positivo. "
            if not possuiSaldo:
                msg += "Saldo insuficiente. "
            if not possuiLimite:
                msg += "Limite de saque excedido. "
            if not possuiSaques:
                msg += "Limite de saques diários alcançado. "
            print(msg)



    elif opcao == "e":
        print(f"==================== EXTRATO ====================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f'Saldo: R$ {saldo:.2f}')
        print("=================================================")

    elif opcao == "q":
        break

    else:
        print(f"Operação inválida, por favor selecione novamente a operação desejada. \n")
