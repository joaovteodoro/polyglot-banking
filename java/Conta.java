import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Conta {

    public static final String AGENCIA           = "0001";
    public static final int    LIMITE_SAQUES      = 3;
    public static final double VALOR_MAXIMO_SAQUE = 500.0;

    private final int     numeroConta;
    private final Usuario usuario;

    private double               saldo        = 0.0;
    private int                  numeroSaques = 0;
    private final List<Movimentacao> extrato  = new ArrayList<>();

    public Conta(int numeroConta, Usuario usuario) {
        this.numeroConta = numeroConta;
        this.usuario     = usuario;
    }

    public int     getNumeroConta() { return numeroConta; }
    public Usuario getUsuario()     { return usuario;     }
    public String  getCpf()        { return usuario.getCpf(); }
    public String  getNome()       { return usuario.getNome(); }
    public double  getSaldo()      { return saldo;        }

    public List<Movimentacao> getExtrato() {
        return Collections.unmodifiableList(extrato);
    }

    public boolean depositar(double valor) {
        if (valor <= 0) return false;
        saldo += valor;
        extrato.add(new Movimentacao(Movimentacao.Tipo.DEPOSITO, valor));
        return true;
    }


    public record SaqueResultado(boolean sucesso, String mensagem) {}

    public SaqueResultado sacar(double valor) {
        if (valor <= 0)
            return new SaqueResultado(false, "Valor inválido.");
        if (valor > VALOR_MAXIMO_SAQUE)
            return new SaqueResultado(false,
                String.format("Limite por saque: R$ %.2f.", VALOR_MAXIMO_SAQUE));
        if (valor > saldo)
            return new SaqueResultado(false, "Saldo insuficiente.");
        if (numeroSaques >= LIMITE_SAQUES)
            return new SaqueResultado(false,
                String.format("Limite de %d saques diários atingido.", LIMITE_SAQUES));

        saldo -= valor;
        numeroSaques++;
        extrato.add(new Movimentacao(Movimentacao.Tipo.SAQUE, valor));
        return new SaqueResultado(true,
                String.format("Saque de R$ %.2f realizado. Saldo: R$ %.2f", valor, saldo));
    }

    public void resetarSaquesDiarios() {
        numeroSaques = 0;
    }

    public String extratoFormatado() {
        String linha    = "-".repeat(51);
        String cabecalho= "-".repeat(21) + " EXTRATO " + "-".repeat(21);
        StringBuilder sb = new StringBuilder();
        sb.append(cabecalho).append("\n\n");

        if (extrato.isEmpty()) {
            sb.append("Nenhuma movimentação registrada.\n");
        } else {
            for (Movimentacao m : extrato)
                sb.append(m).append("\n");
        }

        sb.append(String.format("%n%-30s %20s%n", "SALDO:", String.format("R$ %.2f", saldo)));
        sb.append(linha).append("\n");
        return sb.toString();
    }

    public String info() {
        return "-----------\n"
             + usuario.getNome().toUpperCase() + "   (CPF: " + usuario.getCpf() + ")\n"
             + "Conta: " + numeroConta + "  -  Agência: " + AGENCIA + "\n";
    }

    @Override
    public String toString() {
        return "Agência: " + AGENCIA
             + " | Conta: " + numeroConta
             + " | Titular: " + usuario.getNome()
             + " (CPF: " + usuario.getCpf() + ")";
    }
}