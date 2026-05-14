# Sistema Bancário em Python

Sistema bancário desenvolvido em Python com orientação a objetos. Permite cadastrar usuários, abrir contas e realizar operações financeiras como depósito, saque e consulta de extrato.

---

## Requisitos

- Python 3.10+
- Biblioteca [`validate-docbr`](https://pypi.org/project/validate-docbr/)

---

## Como executar

Crie o ambiente virtual

Ative o ambiente virtual

Baixe as dependências registradas no requirements.txt

```bash
pip install -r requirements.txt
```

Execute o arquivo main.py

```bash
python main.py
```

> Os comandos devem ser executados dentro do diretório sistema_bancario_python\ .

---

## Estrutura de Classes

```
Banco
├── Usuario
│   └── Endereco
└── Conta
```

### `Endereco`
Armazena o endereço completo de um usuário: logradouro, número, bairro, cidade e sigla do estado.

### `Usuario`
Representa um cliente do banco. Possui CPF, nome, data de nascimento e um objeto `Endereco`.

### `Conta`
Conta bancária vinculada a um `Usuario`. Armazena saldo, extrato e histórico de saques.

### `Banco`
Gerencia as coleções de usuários e contas. Responsável por cadastros e buscas.




