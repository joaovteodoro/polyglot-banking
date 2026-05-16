#include <iostream>
#include <string>
#include <string_view>
#include <vector>
#include <optional>
#include <functional>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <algorithm>


static std::string agoraFormatada() {
    std::time_t t  = std::time(nullptr);
    std::tm*    tm = std::localtime(&t);
    char buf[20];
    std::strftime(buf, sizeof(buf), "%d/%m/%Y %H:%M", tm);
    return std::string(buf);
}

static std::string apenasDigitos(std::string_view s) {
    std::string r;
    for (char c : s)
        if (std::isdigit(c)) r += c;
    return r;
}

static bool validarCPF(std::string_view cpf) {
    if (cpf.size() != 11) return false;
    if (std::all_of(cpf.begin(), cpf.end(), [&](char c){ return c == cpf[0]; }))
        return false;

    int soma = 0;
    for (int i = 0; i < 9; i++)
        soma += (cpf[i] - '0') * (10 - i);
    int d1 = (soma * 10) % 11;
    if (d1 == 10 || d1 == 11) d1 = 0;
    if (d1 != (cpf[9] - '0')) return false;

    soma = 0;
    for (int i = 0; i < 10; i++)
        soma += (cpf[i] - '0') * (11 - i);
    int d2 = (soma * 10) % 11;
    if (d2 == 10 || d2 == 11) d2 = 0;
    return d2 == (cpf[10] - '0');
}

static std::string ljust(std::string_view s, int width) {
    if ((int)s.size() >= width) return std::string(s);
    return std::string(s) + std::string(width - s.size(), ' ');
}

static std::string rjust(std::string_view s, int width) {
    if ((int)s.size() >= width) return std::string(s);
    return std::string(width - s.size(), ' ') + std::string(s);
}

class Endereco {
public:
    std::string logradouro, numero, bairro, cidade, siglaEstado;

    Endereco(std::string_view logradouro, std::string_view numero,
             std::string_view bairro,     std::string_view cidade,
             std::string_view siglaEstado)
        : logradouro(logradouro), numero(numero),
          bairro(bairro),         cidade(cidade),
          siglaEstado(siglaEstado)
    {
        std::transform(this->siglaEstado.begin(), this->siglaEstado.end(),
                       this->siglaEstado.begin(), ::toupper);
    }

    std::string str() const {
        return logradouro + ", " + numero + " - "
             + bairro + " - " + cidade + "/" + siglaEstado;
    }
};

class Usuario {
public:
    std::string cpf, nome, dataDeNascimento;
    Endereco    endereco;

    Usuario(std::string_view cpf,  std::string_view nome,
            std::string_view data, const Endereco& endereco)
        : cpf(cpf), nome(nome), dataDeNascimento(data), endereco(endereco) {}

    std::string str() const {
        return "CPF: "      + cpf
             + " | Nome: "  + nome
             + " | Nasc.: " + dataDeNascimento
             + " | End.: "  + endereco.str();
    }
};

class Movimentacao {
public:
    std::string tipo;   // "DEPOSITO" ou "SAQUE"
    double      valor;
    std::string dataHora;

    Movimentacao(std::string_view tipo, double valor)
        : tipo(tipo), valor(valor), dataHora(agoraFormatada()) {}

    std::string str() const {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(2) << valor;
        std::string descricao = std::string(tipo) + ": R$ " + oss.str();
        return ljust(descricao, 30) + rjust(dataHora, 20);
    }
};

class Conta {
public:
    static constexpr std::string_view AGENCIA           = "0001";
    static constexpr int              LIMITE_SAQUE       = 3;
    static constexpr double           VALOR_MAXIMO_SAQUE = 500.0;

    int     numeroConta;
    Usuario usuario;

private:
    double                    _saldo        = 0.0;
    int                       _numeroSaques = 0;
    std::vector<Movimentacao> _extrato;

public:
    Conta(int numeroConta, const Usuario& usuario)
        : numeroConta(numeroConta), usuario(usuario) {}

    double      getSaldo() const { return _saldo;       }
    std::string getCpf()   const { return usuario.cpf;  }
    std::string getNome()  const { return usuario.nome; }

    std::string str() const {
        return "Agencia: " + std::string(AGENCIA)
             + " | Conta: "    + std::to_string(numeroConta)
             + " | Titular: "  + usuario.nome
             + " (CPF: "       + usuario.cpf + ")";
    }

    std::string info() const {
        std::string nomeUpper = usuario.nome;
        std::transform(nomeUpper.begin(), nomeUpper.end(),
                       nomeUpper.begin(), ::toupper);
        return "-----------\n"
             + nomeUpper + "   (CPF: " + usuario.cpf + ")\n"
             + "Conta: " + std::to_string(numeroConta)
             + "  -  Agencia: " + std::string(AGENCIA) + "\n";
    }

    bool depositar(double valor) {
        if (valor <= 0) return false;
        _saldo += valor;
        _extrato.emplace_back("DEPOSITO", valor);
        return true;
    }

    std::pair<bool, std::string> sacar(double valor) {
        if (valor <= 0)
            return {false, "Valor invalido."};

        if (valor > VALOR_MAXIMO_SAQUE) {
            std::ostringstream oss;
            oss << std::fixed << std::setprecision(2) << VALOR_MAXIMO_SAQUE;
            return {false, "O valor limite por saque e de R$ " + oss.str() + "."};
        }
        if (valor > _saldo)
            return {false, "Saldo insuficiente."};
        if (_numeroSaques >= LIMITE_SAQUE)
            return {false, "Limite de " + std::to_string(LIMITE_SAQUE) + " saques diarios atingido."};

        _saldo -= valor;
        _numeroSaques++;
        _extrato.emplace_back("SAQUE", valor);

        std::ostringstream msg;
        msg << std::fixed << std::setprecision(2)
            << "Saque de R$ " << valor
            << " realizado. Saldo: R$ " << _saldo;
        return {true, msg.str()};
    }

    std::string extratoFormatado() const {
        std::string linha(51, '-');
        std::string cab = std::string(21, '-') + " EXTRATO " + std::string(21, '-');
        std::string out = cab + "\n\n";

        if (_extrato.empty()) {
            out += "Nenhuma movimentacao registrada.\n";
        } else {
            for (const auto& mov : _extrato)
                out += mov.str() + "\n";
        }

        std::ostringstream saldo;
        saldo << std::fixed << std::setprecision(2) << _saldo;
        out += "\n" + ljust("SALDO:", 30) + rjust("R$ " + saldo.str(), 20) + "\n";
        out += linha + "\n";
        return out;
    }
};

class Banco {
private:
    std::vector<Usuario> _usuarios;
    std::vector<Conta>   _contas;

public:

    // usuários 
    std::optional<std::reference_wrapper<Usuario>> buscarUsuario(std::string_view cpf) {
        for (auto& u : _usuarios)
            if (u.cpf == cpf) return std::ref(u);
        return std::nullopt;
    }

    bool cadastrarUsuario(std::string_view cpf,  std::string_view nome,
                          std::string_view data,  const Endereco& endereco) {
        if (buscarUsuario(cpf).has_value()) return false;
        _usuarios.emplace_back(cpf, nome, data, endereco);
        return true;
    }

    // contas 
    std::optional<std::reference_wrapper<Conta>> cadastrarConta(std::string_view cpf) {
        if (!buscarUsuario(cpf).has_value()) return std::nullopt;
        _contas.emplace_back((int)_contas.size() + 1, buscarUsuario(cpf)->get());
        return std::ref(_contas.back());
    }

    std::vector<std::reference_wrapper<Conta>> filtrarContas(std::string_view cpf) {
        std::vector<std::reference_wrapper<Conta>> resultado;
        for (auto& c : _contas)
            if (c.getCpf() == cpf) resultado.push_back(std::ref(c));
        return resultado;
    }

    std::optional<std::reference_wrapper<Conta>> buscarConta(std::string_view cpf, int numeroConta) {
        for (auto& c : _contas)
            if (c.getCpf() == cpf && c.numeroConta == numeroConta) return std::ref(c);
        return std::nullopt;
    }

    const std::vector<Conta>& getContas() const { return _contas; }
};

class Menu {
private:
    Banco& banco;

    Endereco coletarEndereco() {
        std::string logr, num, bairro, cidade, sigla;
        std::cout << "Logradouro: ";       std::getline(std::cin, logr);
        std::cout << "Numero: ";           std::getline(std::cin, num);
        std::cout << "Bairro: ";           std::getline(std::cin, bairro);
        std::cout << "Cidade: ";           std::getline(std::cin, cidade);
        std::cout << "Sigla do Estado: ";  std::getline(std::cin, sigla);
        return Endereco(logr, num, bairro, cidade, sigla);
    }

    bool coletarECadastrarUsuario(std::string_view cpf) {
        std::cout << "\nCADASTRAR USUARIO\n";
        std::string nome, data;
        std::cout << "Nome completo: ";                   std::getline(std::cin, nome);
        std::cout << "Data de nascimento (dd/mm/aaaa): "; std::getline(std::cin, data);
        Endereco end = coletarEndereco();

        if (banco.cadastrarUsuario(cpf, nome, data, end)) {
            std::cout << "Usuario cadastrado com sucesso!\n\n";
            return true;
        }
        std::cout << "Usuario ja cadastrado.\n";
        return false;
    }

public:
    explicit Menu(Banco& banco) : banco(banco) {}

    std::optional<std::reference_wrapper<Conta>> menuConta(std::string_view cpf) {
        while (true) {
            std::cout << "\n========== MENU ==========\n"
                         "[e] Entrar em uma conta\n"
                         "[a] Abrir nova conta\n"
                         "[lc] Listar TODAS as contas\n"
                         "[q] Sair\n"
                         "==========================\n"
                         "Digite uma opcao: ";

            std::string opcao;
            std::getline(std::cin, opcao);

            if (opcao == "e") {
                auto contas = banco.filtrarContas(cpf);
                if (contas.empty()) {
                    std::cout << "Nenhuma conta encontrada para este CPF.\n";
                    continue;
                }

                std::cout << "Digite o numero da conta: ";
                std::string numStr;
                std::getline(std::cin, numStr);

                if (int num = 0; [&]{ try { num = std::stoi(numStr); return true; } catch(...){ return false; } }()) {
                    if (auto conta = banco.buscarConta(cpf, num); conta.has_value()) {
                        std::cout << "LOGIN REALIZADO!\n";
                        return conta;
                    }
                    std::cout << "Conta nao encontrada.\n";
                } else {
                    std::cout << "Numero invalido.\n";
                }

            } else if (opcao == "a") {
                if (!banco.buscarUsuario(cpf).has_value()) {
                    std::cout << "Usuario nao cadastrado.\n";
                    coletarECadastrarUsuario(cpf);
                }
                if (auto nova = banco.cadastrarConta(cpf); nova.has_value())
                    std::cout << "Conta criada com sucesso!\n" << nova->get().str() << "\n";
                else
                    std::cout << "Nao foi possivel criar a conta.\n";

            } else if (opcao == "lc") {
                const auto& todas = banco.getContas();
                if (todas.empty()) std::cout << "Nenhuma conta cadastrada.\n";
                else for (const auto& c : todas) std::cout << c.info();

            } else if (opcao == "q") {
                std::cout << "Obrigado pela confianca!\n";
                return std::nullopt;

            } else {
                std::cout << "Opcao invalida!\n";
            }
        }
    }

    void menuOperacoes(std::string_view cpf, Conta& conta) {
        while (true) {
            std::cout << "\n========== MENU ==========\n"
                         " [d]  Depositar\n"
                         " [s]  Sacar\n"
                         " [e]  Extrato\n"
                         " [lc] Listar minhas contas\n"
                         " [q]  Sair\n"
                         "==========================\n"
                         "Escolha: ";

            std::string opcao;
            std::getline(std::cin, opcao);

            if (opcao == "d") {
                std::cout << "Valor do deposito: R$ ";
                std::string valStr;
                std::getline(std::cin, valStr);
                try {
                    double val = std::stod(valStr);
                    if (conta.depositar(val)) {
                        std::ostringstream oss;
                        oss << std::fixed << std::setprecision(2)
                            << "Deposito de R$ " << val
                            << " realizado. Saldo: R$ " << conta.getSaldo();
                        std::cout << oss.str() << "\n";
                    } else {
                        std::cout << "Nao e possivel depositar valor invalido ou negativo.\n";
                    }
                } catch (...) { std::cout << "Valor invalido.\n"; }

            } else if (opcao == "s") {
                std::cout << "Valor do saque: R$ ";
                std::string valStr;
                std::getline(std::cin, valStr);
                try {
                    double val = std::stod(valStr);
                    auto [sucesso, mensagem] = conta.sacar(val);
                    if (sucesso) std::cout << mensagem << "\n";
                    else         std::cout << "Erro: " << mensagem << "\n";
                } catch (...) { std::cout << "Valor invalido.\n"; }

            } else if (opcao == "e") {
                std::cout << conta.extratoFormatado();

            } else if (opcao == "lc") {
                for (auto& c : banco.filtrarContas(cpf))
                    std::cout << c.get().info();

            } else if (opcao == "q") {
                std::cout << "Encerrando operacao.\n";
                break;

            } else {
                std::cout << "Opcao invalida!\n";
            }
        }
    }
};

int main() {
    Banco banco;
    Menu  menu(banco);

    while (true) {
        std::cout << "\nDigite o seu CPF (ou sair): ";
        std::string entrada;
        std::getline(std::cin, entrada);

        if (entrada == "sair") {
            std::cout <<"Obrigado pela confianca!\n";
            break;
        }

        std::string cpf = apenasDigitos(entrada);

        if (!validarCPF(cpf)) {
            std::cout << "CPF invalido!\n";
            continue;
        }

        auto conta = menu.menuConta(cpf);
        if (!conta.has_value()) break;

        menu.menuOperacoes(cpf, conta->get());
    }

    return 0;
}