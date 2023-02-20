import textwrap

def depositar(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido")

    return saldo, extrato

def sacar(*, valor, saldo, extrato, limite, numero_saques, LIMITE_SAQUES):
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
    return saldo, extrato

def func_extrato(saldo, extrato):
    print(f"==================== EXTRATO ====================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f'Saldo: R$ {saldo:.2f}')
    print("=================================================")

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu)).lower()

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def listar_usuarios(usuarios):
    senhaAdmin = input("Insira a senha de administrador: ")

    #Observação: Não coloque senhas diretamente no código, esta prática é totalmente errada e perigosa, isso é apenas um exemplo bobo para uma função protegida
    #normalmente a senha seria obtida de um banco de dados para não ficar exposta em um código fonte
    if(senhaAdmin == "senhaMocadaTotalmenteSegura"):
        for usuario in usuarios:
            linha = f"""\
                Nome:\t\t\t{usuario['nome']}
                CPF:\t\t\t{usuario['cpf']}
                Data de Nascimento:\t{usuario["data_nascimento"]}
                Endereco:\t\t{usuario["endereco"]}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))
    else:
        print("Acesso negado!")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0;

    usuarios = []
    contas = []
    

    while True:

        opcao = menu()
        print()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(valor, saldo, extrato)


        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                valor = valor,
                saldo = saldo,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                LIMITE_SAQUES = LIMITE_SAQUES
            )

        elif opcao == "e":
            func_extrato(saldo, extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "q":
            break

        else:
            print(f"Operação inválida, por favor selecione novamente a operação desejada. \n")

main()