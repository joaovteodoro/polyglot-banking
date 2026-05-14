import datetime
import re
from validate_docbr import CPF

class Endereco:
    def __init__(self, logradouro: str, numero: str, bairro: str,
                 cidade: str, sigla_estado: str):
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.sigla_estado = sigla_estado.upper()

    def __str__(self) -> str:
        return (
            f"{self.logradouro}, {self.numero} - "
            f"{self.bairro} - {self.cidade}/{self.sigla_estado}"
        )

class Usuario:
    def __init__(self, cpf: str, nome: str,
                 data_de_nascimento: str, endereco: Endereco):
        self.cpf = cpf
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
        self.endereco = endereco

    def __str__(self) -> str:
        return (
            f"CPF: {self.cpf} | Nome: {self.nome} | "
            f"Nascimento: {self.data_de_nascimento} | Endereço: {self.endereco}"
        )

class Conta:
    """
    Representa uma conta bancária vinculada a um Usuario.

    Correções aplicadas:
    - Recebe objeto Usuario em vez de cpf/nome soltos (sem duplicação de dados).
    - Atributos de instância definidos apenas no __init__.
    - data_atual capturada dentro dos próprios métodos (sem variável global).
    - Método mostrar_extrato retorna string em vez de imprimir diretamente.
    - LIMITE_SAQUE permanece como constante de classe (maiúsculas).
    """

    LIMITE_SAQUE = 3
    VALOR_MAXIMO_SAQUE = 500.0

    def __init__(self, numero_conta: int, usuario: Usuario):
        self.AGENCIA = "0001"
        self.numero_conta = numero_conta
        self.usuario = usuario          # referência ao objeto, sem duplicar dados
        self._saldo = 0.0
        self._extrato: list[str] = []
        self._numero_saques = 0         # prefixo _ indica atributo de instância interno

    #  propriedades de leitura 

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def cpf(self) -> str:
        """Atalho para manter compatibilidade com filtros por CPF."""
        return self.usuario.cpf

    @property
    def nome(self) -> str:
        return self.usuario.nome

    #  representação 

    def __str__(self) -> str:
        return (
            f"Agência: {self.AGENCIA} | "
            f"Conta: {self.numero_conta} | "
            f"Titular: {self.usuario.nome} (CPF: {self.usuario.cpf})"
        )

    def info(self) -> str:
        """Retorna string formatada para exibição em listagens."""
        return (
            f"-----------\n"
            f"{self.usuario.nome.upper()}   (CPF: {self.usuario.cpf})\n"
            f"Conta: {self.numero_conta}  -  Agência: {self.AGENCIA}\n"
        )

    #  operações 

    def depositar(self, valor: float) -> bool:
        """
        Realiza depósito.
        Retorna True em sucesso, False em falha.
        Mensagens de UI ficam nas funções de menu.
        """
        if valor <= 0:
            return False

        self._saldo += valor
        data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self._extrato.append(f"DEPÓSITO: R$ {valor:.2f} - {data}")
        return True

    def sacar(self, valor: float) -> tuple[bool, str]:
        """
        Realiza saque.
        Retorna (sucesso: bool, mensagem: str) para que a UI exiba o resultado.
        """
        if valor <= 0:
            return False, "Valor inválido."
        if valor > self.VALOR_MAXIMO_SAQUE:
            return False, f"O valor limite por saque é de R$ {self.VALOR_MAXIMO_SAQUE:.2f}."
        if valor > self._saldo:
            return False, "Saldo insuficiente."
        if self._numero_saques >= self.LIMITE_SAQUE:
            return False, f"Limite de {self.LIMITE_SAQUE} saques diários atingido."

        self._saldo -= valor
        self._numero_saques += 1
        data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self._extrato.append(f"SAQUE:    R$ {valor:.2f} - {data}")
        return True, f"Saque de R$ {valor:.2f} realizado. Saldo: R$ {self._saldo:.2f}"

    def extrato(self) -> str:
        """Retorna o extrato formatado como string."""
        linha = "-" * 51
        cabecalho = f"{'-' * 21} EXTRATO {'-' * 21}"
        linhas = [cabecalho, ""]

        if not self._extrato:
            linhas.append("Nenhuma movimentação registrada.")
        else:
            for operacao in self._extrato:
                descricao, data = operacao.split(" - ", 1)
                linhas.append(descricao.ljust(30) + data.rjust(20))

        linhas += ["", f"SALDO: R$ {self._saldo:.2f}", linha, ""]
        return "\n".join(linhas)

class Banco:
    """
    Gerencia coleções de usuários e contas.
    Recebe dados prontos (sem input()); quem chama é responsável por coletar.
    """

    def __init__(self):
        self._usuarios: list[Usuario] = []
        self._contas: list[Conta] = []

    #  usuários 

    def buscar_usuario(self, cpf: str) -> Usuario | None:
        for usuario in self._usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def cadastrar_usuario(self, cpf: str, nome: str,
                          data_de_nascimento: str, endereco: Endereco) -> bool:
        if self.buscar_usuario(cpf):
            return False   # já existe
        self._usuarios.append(Usuario(cpf, nome, data_de_nascimento, endereco))
        return True

    #  contas 

    def cadastrar_conta(self, cpf: str) -> Conta | None:
        usuario = self.buscar_usuario(cpf)
        if not usuario:
            return None
        numero_conta = len(self._contas) + 1
        nova_conta = Conta(numero_conta, usuario)
        self._contas.append(nova_conta)
        return nova_conta

    def filtrar_contas(self, cpf: str) -> list[Conta]:
        return [c for c in self._contas if c.cpf == cpf]

    def buscar_conta(self, cpf: str, numero_conta: int) -> Conta | None:
        for conta in self.filtrar_contas(cpf):
            if conta.numero_conta == numero_conta:
                return conta
        return None

    @property
    def contas(self) -> list[Conta]:
        return list(self._contas)   # cópia defensiva



def _coletar_endereco() -> Endereco:
    logradouro = input("Logradouro: ")
    numero     = input("Número: ")
    bairro     = input("Bairro: ")
    cidade     = input("Cidade: ")
    sigla      = input("Sigla do Estado: ")
    return Endereco(logradouro, numero, bairro, cidade, sigla)

def _coletar_e_cadastrar_usuario(banco: Banco, cpf: str) -> bool:
    print("─── CADASTRAR USUÁRIO ───")
    nome               = input("Nome completo: ")
    data_de_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco           = _coletar_endereco()
    if banco.cadastrar_usuario(cpf, nome, data_de_nascimento, endereco):
        print("Usuário cadastrado com sucesso!\n")
        return True
    print("Usuário já cadastrado.")
    return False

def menu_conta(banco: Banco, cpf: str):

    while True:
        print(
            "\n========== MENU ==========\n"
            "[e] Entrar em uma conta\n"
            "[a] Abrir nova conta\n"
            "[lc] Listar TODAS as contas\n"
            "[q] Sair\n"
            "=========================="
        )
        opcao = input("Digite uma opção: ").strip().lower()

        if opcao == "e":
            contas_usuario = banco.filtrar_contas(cpf)
            if not contas_usuario:
                print("Nenhuma conta encontrada para este CPF.")
                continue

            try:
                numero = int(input("Digite o número da conta: "))
            except ValueError:
                print("Número de conta inválido.")
                continue

            conta = banco.buscar_conta(cpf, numero)
            if not conta:
                print("Conta não encontrada.")
                continue

            print("LOGIN REALIZADO!")
            return cpf, conta

        elif opcao == "a":
            if not banco.buscar_usuario(cpf):
                print("Usuário não cadastrado.")
                _coletar_e_cadastrar_usuario(banco, cpf)

            nova = banco.cadastrar_conta(cpf)
            if nova:
                print(f"Conta criada com sucesso!\n{nova}")
            else:
                print("Não foi possível criar a conta.")

        elif opcao == "lc":
            contas = banco.contas
            if contas:
                for c in contas:
                    print(c.info())
            else:
                print("Nenhuma conta cadastrada.")

        elif opcao == "q":
            print("Obrigado pela confiança!")
            return "quit"

        else:
            print("Opção inválida!")

def menu_operacoes(banco: Banco, cpf: str, conta: Conta) -> None:
    while True:
        print(
            "\n========== MENU ==========\n"
            " [d]  Depositar\n"
            " [s]  Sacar\n"
            " [e]  Extrato\n"
            " [lc] Listar minhas contas\n"
            " [q]  Sair\n"
            "=========================="
        )
        opcao = input("Escolha: ").strip().lower()

        if opcao == "d":
            try:
                valor = float(input("Valor do depósito: R$ "))
            except ValueError:
                print("Valor inválido.")
                continue

            if conta.depositar(valor):
                print(f"Depósito de R$ {valor:.2f} realizado. Saldo: R$ {conta.saldo:.2f}")
            else:
                print("Não é possível depositar valor inválido ou negativo.")

        elif opcao == "s":
            try:
                valor = float(input("Valor do saque: R$ "))
            except ValueError:
                print("Valor inválido.")
                continue

            sucesso, mensagem = conta.sacar(valor)
            print(mensagem if sucesso else f"Erro: {mensagem}")

        elif opcao == "e":
            print(conta.extrato())

        elif opcao == "lc":
            for c in banco.filtrar_contas(cpf):
                print(c.info())

        elif opcao == "q":
            print("Encerrando operação.")
            break

        else:
            print("Opção inválida!")


def main() -> None:
    banco = Banco()
    validador_cpf = CPF()

    while True:
        cpf_digitado = input("\nDigite o seu CPF: ")
        cpf_digitado = re.sub(r'\D', '', cpf_digitado)

        if not validador_cpf.validate(cpf_digitado):
            print("CPF inválido!")
            continue

        resultado = menu_conta(banco, cpf_digitado)

        if resultado == "quit":
            break
        if resultado is None:
            continue

        cpf, conta = resultado
        menu_operacoes(banco, cpf, conta)

if __name__ == "__main__":
    main()