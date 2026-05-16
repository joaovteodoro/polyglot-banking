import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Movimentacao {

    public enum Tipo { DEPOSITO, SAQUE }

    private static final DateTimeFormatter FMT =
            DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");

    private final Tipo          tipo;
    private final double        valor;
    private final LocalDateTime dataHora;

    public Movimentacao(Tipo tipo, double valor) {
        this.tipo     = tipo;
        this.valor    = valor;
        this.dataHora = LocalDateTime.now();
    }

    public Tipo          getTipo()    { return tipo;    }
    public double        getValor()   { return valor;   }
    public LocalDateTime getDataHora(){ return dataHora;}

    @Override
    public String toString() {
        String descricao = (tipo == Tipo.DEPOSITO ? "DEPÓSITO" : "SAQUE   ")
                         + String.format(": R$ %8.2f", valor);
        return String.format("%-30s %20s", descricao, dataHora.format(FMT));
    }
}