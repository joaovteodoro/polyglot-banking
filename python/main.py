import datetime
import re

from datetime import date
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
                 data_de_nascimento: date, endereco: Endereco):
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

    LIMITE_SAQUE = 3
    VALOR_MAXIMO_SAQUE = 500.0

    def __init__(self, numero_conta: int, usuario: Usuario):
        self.AGENCIA = "0001"
        self.numero_conta = numero_conta
        self.usuario = usuario         
        self._saldo = 0.0
        self._extrato: list[Movimentacao] = []
        self._numero_saques = 0         

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def cpf(self) -> str:
        return self.usuario.cpf

    @property
    def nome(self) -> str:
        return self.usuario.nome

    def __str__(self) -> str:
        return (
            f"Agência: {self.AGENCIA} | "
            f"Conta: {self.numero_conta} | "
            f"Titular: {self.usuario.nome} (CPF: {self.usuario.cpf})"
        )

    def info(self) -> str:
        return (
            f"-----------\n"
            f"{self.usuario.nome.upper()}   (CPF: {self.usuario.cpf})\n"
            f"Conta: {self.numero_conta}  -  Agência: {self.AGENCIA}\n"
        )

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            return False

        self._saldo += valor
        self._extrato.append(Movimentacao("DEPOSITO", valor))
        return True

    def sacar(self, valor: float) -> tuple[bool, str]:

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
        self._extrato.append(Movimentacao("SAQUE", valor))
        return True, f"Saque de R$ {valor:.2f} realizado. Saldo: R$ {self._saldo:.2f}"

    def extrato(self) -> str:
        linha = "-" * 51
        cabecalho = f"{'-' * 21} EXTRATO {'-' * 21}"
        linhas = [cabecalho, ""]

        if not self._extrato:
            linhas.append("Nenhuma movimentação registrada.")
        else:
            for operacao in self._extrato:
                linhas.append(str(operacao))

        linhas += ["", f"SALDO: R$ {self._saldo:.2f}", linha, ""]
        return "\n".join(linhas)

class Movimentacao:

    def __init__(self, tipo: str, valor: float):
        self.tipo    = tipo                              # "DEPÓSITO" ou "SAQUE"
        self.valor   = valor
        self.data    = datetime.datetime.now()           # guarda o objeto, não a string

    def __str__(self) -> str:
        data_fmt = self.data.strftime("%d/%m/%Y %H:%M")
        descricao = f"{self.tipo}: R$ {self.valor:.2f}"
        return descricao.ljust(30) + data_fmt.rjust(20)


class Banco:
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

class Menu:

    def __init__(self, banco: Banco):  
        self.banco = banco

    def _coletar_endereco(self) -> Endereco:
        logradouro = input("Logradouro: ")
        numero     = input("Número: ")
        bairro     = input("Bairro: ")
        cidade     = input("Cidade: ")
        sigla      = input("Sigla do Estado: ")
        return Endereco(logradouro, numero, bairro, cidade, sigla)

    def _coletar_e_cadastrar_usuario(self, cpf: str) -> bool:
        print(f"\nCADASTRAR USUÁRIO")
        nome               = input("Nome completo: ").upper()
        data_de_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
        endereco           = self._coletar_endereco()
        if self.banco.cadastrar_usuario(cpf, nome, data_de_nascimento, endereco):
            print("Usuário cadastrado com sucesso!\n")
            return True
        print("Usuário já cadastrado.")
        return False
    
    def menu_conta(self, cpf: str):

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
                contas_usuario = self.banco.filtrar_contas(cpf)
                if not contas_usuario:
                    print("Nenhuma conta encontrada para este CPF.")
                    continue

                try:
                    numero = int(input("Digite o número da conta: "))
                except ValueError:
                    print("Número de conta inválido.")
                    continue

                conta = self.banco.buscar_conta(cpf, numero)
                if not conta:
                    print("Conta não encontrada.")
                    continue

                print("LOGIN REALIZADO!")
                return cpf, conta

            elif opcao == "a":
                if not self.banco.buscar_usuario(cpf):
                    print("Usuário não cadastrado.")
                    self._coletar_e_cadastrar_usuario(cpf)

                nova = self.banco.cadastrar_conta(cpf)
                if nova:
                    print(f"Conta criada com sucesso!\n{nova}")
                else:
                    print("Não foi possível criar a conta.")

            elif opcao == "lc":
                contas = self.banco.contas
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

    def menu_operacoes(self, cpf: str, conta: Conta) -> None:
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
                for c in self.banco.filtrar_contas(cpf):
                    print(c.info())

            elif opcao == "q":
                print("Encerrando operação.")
                break

            else:
                print("Opção inválida!")


def main() -> None:
    banco = Banco()
    validador_cpf = CPF()
    menu_banco = Menu(banco)

    while True:
        cpf_digitado = input("\nDigite o seu CPF (ou sair): ")

        if cpf_digitado == "sair":
            print("Obrigado pela confiança!")
            break

        cpf_digitado = re.sub(r'\D', '', cpf_digitado)

        if not validador_cpf.validate(cpf_digitado):
            print("CPF inválido!")
            continue

        resultado = menu_banco.menu_conta(cpf_digitado)

        if resultado == "quit":
            break
        if resultado is None:
            continue

        cpf, conta = resultado
        menu_banco.menu_operacoes(cpf, conta)

if __name__ == "__main__":
    main()