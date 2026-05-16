import java.util.List;
import java.util.Optional;
import java.util.Scanner;


public class MenuUI {

    private final Banco   banco;
    private final Scanner scanner;

    public MenuUI(Banco banco, Scanner scanner) {
        this.banco   = banco;
        this.scanner = scanner;
    }

    public void iniciar() {
        while (true) {
            String cpf = lerCpf();
            if (cpf == null) break;     

            boolean continuar = menuConta(cpf);
            if (!continuar) break;
        }
        System.out.println("Obrigado pela confiança!");
    }

    private boolean menuConta(String cpf) {
        while (true) {
            System.out.println("""

                    ========== MENU ==========
                    [e]  Entrar em uma conta
                    [a]  Abrir nova conta
                    [lc] Listar TODAS as contas
                    [q]  Sair
                    ==========================""");

            String opcao = scanner.nextLine().strip().toLowerCase();

            switch (opcao) {
                case "e" -> {
                    Optional<Conta> conta = selecionarConta(cpf);
                    if (conta.isPresent()) {
                        System.out.println("LOGIN REALIZADO!");
                        menuOperacoes(cpf, conta.get());
                    }
                }
                case "a" -> abrirConta(cpf);
                case "lc" -> listarTodasContas();
                case "q"  -> { return false; }
                default   -> System.out.println("Opção inválida!");
            }
        }
    }

    private void menuOperacoes(String cpf, Conta conta) {
        while (true) {
            System.out.println("""

                    ========== MENU ==========
                     [d]  Depositar
                     [s]  Sacar
                     [e]  Extrato
                     [lc] Listar minhas contas
                     [q]  Sair
                    ==========================""");

            String opcao = scanner.nextLine().strip().toLowerCase();

            switch (opcao) {
                case "d"  -> depositar(conta);
                case "s"  -> sacar(conta);
                case "e"  -> System.out.println(conta.extratoFormatado());
                case "lc" -> banco.filtrarContas(cpf).forEach(c -> System.out.println(c.info()));
                case "q"  -> { System.out.println("Encerrando operação."); return; }
                default   -> System.out.println("Opção inválida!");
            }
        }
    }

    private void depositar(Conta conta) {
        double valor = lerValor("Valor do depósito: R$ ");
        if (valor <= 0) { System.out.println("Valor inválido."); return; }

        if (conta.depositar(valor))
            System.out.printf("Depósito de R$ %.2f realizado. Saldo: R$ %.2f%n",
                              valor, conta.getSaldo());
        else
            System.out.println("Não é possível depositar valor inválido ou negativo.");
    }

    private void sacar(Conta conta) {
        double valor = lerValor("Valor do saque: R$ ");
        if (valor <= 0) { System.out.println("Valor inválido."); return; }

        Conta.SaqueResultado resultado = conta.sacar(valor);
        System.out.println(resultado.sucesso() ? resultado.mensagem()
                                               : "Erro: " + resultado.mensagem());
    }

    private Optional<Conta> selecionarConta(String cpf) {
        List<Conta> contas = banco.filtrarContas(cpf);
        if (contas.isEmpty()) {
            System.out.println("Nenhuma conta encontrada para este CPF.");
            return Optional.empty();
        }
        System.out.println("Suas contas:");
        contas.forEach(c -> System.out.println(c.info()));

        int numero = lerInt("Digite o número da conta: ");
        Optional<Conta> conta = banco.buscarConta(cpf, numero);
        if (conta.isEmpty()) System.out.println("Conta não encontrada.");
        return conta;
    }

    private void abrirConta(String cpf) {
        if (banco.buscarUsuario(cpf).isEmpty()) {
            System.out.println("Usuário não cadastrado. Vamos cadastrá-lo agora.");
            cadastrarUsuario(cpf);
        }
        banco.cadastrarConta(cpf).ifPresentOrElse(
            nova -> System.out.println("Conta criada com sucesso!\n" + nova),
            ()   -> System.out.println("Não foi possível criar a conta.")
        );
    }

    private void cadastrarUsuario(String cpf) {
        System.out.println("─── CADASTRAR USUÁRIO ───");
        try {
            System.out.print("Nome completo: ");
            String nome = scanner.nextLine();

            System.out.print("Data de nascimento (dd/MM/yyyy): ");
            String dataNasc = scanner.nextLine();

            Endereco endereco = coletarEndereco();

            if (banco.cadastrarUsuario(cpf, nome, dataNasc, endereco))
                System.out.println("Usuário cadastrado com sucesso!\n");
            else
                System.out.println("Usuário já cadastrado.");

        } catch (IllegalArgumentException e) {
            System.out.println("Erro ao cadastrar: " + e.getMessage());
        }
    }

    private Endereco coletarEndereco() {
        System.out.print("Logradouro: ");  String logr = scanner.nextLine();
        System.out.print("Número: ");      String num  = scanner.nextLine();
        System.out.print("Bairro: ");      String bairro = scanner.nextLine();
        System.out.print("Cidade: ");      String cidade = scanner.nextLine();
        System.out.print("Sigla do Estado: "); String sigla = scanner.nextLine();
        return new Endereco(logr, num, bairro, cidade, sigla);
    }

    private void listarTodasContas() {
        List<Conta> todas = banco.getContas();
        if (todas.isEmpty()) System.out.println("Nenhuma conta cadastrada.");
        else todas.forEach(c -> System.out.println(c.info()));
    }

    private String lerCpf() {
        while (true) {
            System.out.print("\nDigite o seu CPF (ou 'sair'): ");
            String entrada = scanner.nextLine().strip();
            if (entrada.equalsIgnoreCase("sair")) return null;

            String cpfLimpo = entrada.replaceAll("\\D", "");

            boolean valido = validarCpf(cpfLimpo);

            if (!valido) {
                System.out.println("CPF inválido!");
                continue;
            }
            return cpfLimpo;
        }
    }

    private double lerValor(String prompt) {
        System.out.print(prompt);
        try   { return Double.parseDouble(scanner.nextLine().replace(",", ".")); }
        catch (NumberFormatException e) { return -1; }
    }

    private int lerInt(String prompt) {
        System.out.print(prompt);
        try   { return Integer.parseInt(scanner.nextLine().strip()); }
        catch (NumberFormatException e) { return -1; }
    }

    // verifica se o numero é um CPF real 
    private boolean validarCpf(String cpf) {
        if (cpf == null || cpf.length() != 11 || cpf.matches("(\\d)\\1{10}")) return false;

        int soma = 0;
        for (int i = 0; i < 9; i++) soma += (cpf.charAt(i) - '0') * (10 - i);
        int dig1 = 11 - (soma % 11);
        if (dig1 >= 10) dig1 = 0;

        soma = 0;
        for (int i = 0; i < 10; i++) soma += (cpf.charAt(i) - '0') * (11 - i);
        int dig2 = 11 - (soma % 11);
        if (dig2 >= 10) dig2 = 0;

        return dig1 == (cpf.charAt(9) - '0') && dig2 == (cpf.charAt(10) - '0');
    }
}
