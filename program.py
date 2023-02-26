import textwrap
import abc 
import datetime

class Conta:
    _agencia = "001"

    def __init__(self, cliente, numero):
        self._cliente = cliente
        self._numero = numero
        self._saldo = 0.0
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def numero(self):
        return self._numero

    @property
    def historico(self):
        return self._historico
    
    def mostrar_historico(self):
        string = f"\n=================================================\n"
        string += f"Saldo:  {self._saldo:.2f}\n"
        string += f"=================================================\n"
        string += self._historico.__str__()
        print(string)
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    def sacar(self, valor):
        valorPositivo = valor > 0
        possuiSaldo = valor <= self._saldo


        if valorPositivo and possuiSaldo:
            self._saldo -= valor
            return True

        if not valorPositivo:
            print("Operação falhou! O valor informado é inválido")
        else:
            print("Operação falhou! Saldo insuficiente!")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        
        print("Operação falhou! O valor informado é inválido")
        return False;

class ContaCorrente(Conta):
    def __init__(self, limite=500, limite_saques=3, **kw):
        self._limite = limite
        self._limite_saques = limite_saques
        super().__init__(**kw)

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\nOperação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self):
        return self._contas
    
    @property
    def endereco(self):
        return self._endereco

    def realizar_transacao(self, conta: Conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta:Conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, **kw):
        self._cpf = cpf
        self._nome = nome 
        self._data_nascimento = data_nascimento
        super().__init__(**kw)

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": str(transacao.valor),
                "data": datetime.datetime.now().strftime(f"%d/%m/%Y %H:%M:%S"),
            }
        )

    def __str__(self):
        str = ""
        for transacao in self._transacoes:
            str += transacao["tipo"]
            str += f": R$ "
            str += transacao["valor"]
            str += f". Data: "
            str += transacao["data"]
            str += f'\n'
        return str

class Transacao(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):

    def __init__(self, valor:float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta:Conta):
        if conta.depositar(valor=self._valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta:Conta):
        if conta.sacar(valor=self._valor):
            conta.historico.adicionar_transacao(self)

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
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento_str = input("Informe a data de nascimento (dd/mm/aaaa): ")
    numeros = data_nascimento_str.split("/")
    data_nascimento = datetime.date(int(numeros[2]), int(numeros[1]), int(numeros[0]))
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(cpf = cpf, nome = nome, data_nascimento = data_nascimento, endereco = endereco)
    usuarios.append(cliente)

    print(f"\n=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = ContaCorrente(cliente=usuario, numero=numero_conta)
        usuario.adicionar_conta(conta)
        print("\n=== Conta criada com sucesso! ===")
        return conta

    print("\nUsuário não encontrado!")


def listar_contas(usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        contas = usuario.contas
        for conta in contas:
            linha = f"""\
                Agência:\t{conta.agencia}
                C/C:\t\t{conta.numero}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

        return contas
    
    print("\nUsuário não encontrado!")

def listar_usuarios(usuarios):
    senhaAdmin = input("Insira a senha de administrador: ")

    #Observação: Não coloque senhas diretamente no código, esta prática é totalmente errada e perigosa, isso é apenas um exemplo bobo para uma função protegida
    #normalmente a senha seria obtida de um banco de dados para não ficar exposta em um código fonte
    if(senhaAdmin == "senhaMocadaTotalmenteSegura"):
        for usuario in usuarios:
            linha = f"""\
                Nome:\t\t\t{usuario.nome}
                CPF:\t\t\t{usuario.cpf}
                Data de Nascimento:\t{usuario.data_nascimento}
                Endereco:\t\t{usuario.endereco}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))
    else:
        print("Acesso negado!")

def selecionar_conta(usuarios):
    contas = listar_contas(usuarios)
    if contas:
        numero_conta = input("Informe o número da conta: ")
        conta_filtrada = [conta for conta in contas if conta.numero == numero_conta]
        return conta_filtrada[0] if conta_filtrada else None
    return None

def depositar(valor, usuarios):
    conta = selecionar_conta(usuarios)
    if conta:
        usuario:Cliente = conta.cliente
        transacao = Deposito(valor)
        usuario.realizar_transacao(conta, transacao)
        return
    print("Operação falhou!")

def sacar(valor, usuarios):
    conta = selecionar_conta(usuarios)
    if conta:
        usuario:Cliente = conta.cliente
        transacao = Saque(valor)
        usuario.realizar_transacao(conta, transacao)
        return
    print("Operação falhou!")

def func_extrato(usuarios):
    conta:Conta = selecionar_conta(usuarios)
    if conta:
        conta.mostrar_historico()
        return
    
    print("Conta inválida!")

def main():

    usuarios = []
    contas =[]

    while True:

        opcao = menu()
        print()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            depositar(valor=valor, usuarios=usuarios)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            sacar(valor=valor, usuarios=usuarios)

        elif opcao == "e":
            func_extrato(usuarios=usuarios)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = str(len(contas) + 1)
            conta = criar_conta(numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(usuarios)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "q":
            break

        else:
            print(f"Operação inválida, por favor selecione novamente a operação desejada. \n")

main()