# polyglot-banking

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=c%2B%2B&logoColor=white)

Sistema bancário desenvolvido como projeto do Bootcamp em parceria com a DIO. O objetivo inicial era implementar o sistema em Python com orientação a objetos — decidi reimplementar o mesmo sistema em **Java** e **C++**, explorando como cada linguagem lida com os mesmos conceitos de POO.
---

## Organização do repositório

O repositório possui 3 diretórios, um por linguagem:

```
polyglot-banking/
├── python/
├── java/
└── cpp/
```

Cada diretório contém um `README.md` próprio com instruções de como compilar/executar o código.

---

## Como rodar (exemplo rápido — Python)

Consulte o README de cada linguagem para os pré-requisitos e comandos específicos.

---

## Funcionalidades

### Autenticação por CPF
Ao iniciar, o sistema solicita e valida um CPF.

### Menu de Conta

| Opção | Descrição |
|---|---|
| `[e]` Entrar em uma conta | Acessa uma conta existente pelo número |
| `[a]` Abrir nova conta | Cria uma nova conta para o CPF informado |
| `[lc]` Listar todas as contas | Exibe todas as contas cadastradas no banco |
| `[q]` Sair | Encerra o programa |

> Se o CPF não estiver cadastrado, o sistema solicita nome, data de nascimento e endereço antes de criar a conta.

### Menu de Operações

| Opção | Descrição |
|---|---|
| `[d]` Depositar | Adiciona saldo à conta |
| `[s]` Sacar | Retira valor da conta |
| `[e]` Extrato | Exibe histórico de movimentações e saldo atual |
| `[lc]` Listar minhas contas | Lista todas as contas vinculadas ao CPF |
| `[q]` Sair | Retorna ao menu anterior |

---

## Regras de Negócio

### Depósito
- O valor deve ser maior que zero.

### Saque
- O valor deve ser maior que zero.
- Limite máximo por saque: **R$ 500,00**.
- O saldo disponível deve ser suficiente.
- Máximo de **3 saques por dia**.

### Extrato
- Exibe todas as movimentações com data e hora.
- Exibe o saldo atual ao final.
- Caso não haja movimentações, exibe `"Nenhuma movimentação registrada."`.

---

## Licença

Distribuído sob a licença [MIT](LICENSE). Livre para usar, copiar, modificar e distribuir.