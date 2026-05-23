package model;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

public class Usuario {

    private static final DateTimeFormatter FMT_DATA =
            DateTimeFormatter.ofPattern("dd/MM/yyyy");

    private final String     cpf;
    private final String     nome;
    private final LocalDate  dataDeNascimento;
    private final Endereco   endereco;

    public Usuario(String cpf, String nome,
                   String dataDeNascimento, Endereco endereco) {

        String cpfLimpo = cpf.replaceAll("\\D", "");
        if (!isCpfValido(cpfLimpo))
            throw new IllegalArgumentException("CPF inválido: " + cpf);

        if (nome == null || nome.isBlank())
            throw new IllegalArgumentException("Nome não pode ser vazio.");

        LocalDate nascimento;
        try {
            nascimento = LocalDate.parse(dataDeNascimento, FMT_DATA);
        } catch (DateTimeParseException e) {
            throw new IllegalArgumentException(
                    "Data inválida (esperado dd/MM/yyyy): " + dataDeNascimento);
        }
        if (nascimento.isAfter(LocalDate.now()))
            throw new IllegalArgumentException("Data de nascimento futura: " + dataDeNascimento);

        this.cpf              = cpfLimpo;
        this.nome             = nome.trim();
        this.dataDeNascimento = nascimento;
        this.endereco         = endereco;
    }

    public String    getCpf()              { return cpf;              }
    public String    getNome()             { return nome;             }
    public LocalDate getDataDeNascimento() { return dataDeNascimento; }
    public Endereco  getEndereco()         { return endereco;         }

    @Override
    public String toString() {
        return "CPF: "       + cpf
             + " | Nome: "   + nome
             + " | Nasc.: "  + dataDeNascimento.format(FMT_DATA)
             + " | End.: "   + endereco;
    }


    private static boolean isCpfValido(String cpf) {
        if (cpf.length() != 11) return false;
        if (cpf.chars().distinct().count() == 1) return false; 

        int soma = 0;
        for (int i = 0; i < 9; i++)
            soma += Character.getNumericValue(cpf.charAt(i)) * (10 - i);
        int d1 = (soma * 10) % 11;
        if (d1 == 10 || d1 == 11) d1 = 0;
        if (d1 != Character.getNumericValue(cpf.charAt(9))) return false;

        soma = 0;
        for (int i = 0; i < 10; i++)
            soma += Character.getNumericValue(cpf.charAt(i)) * (11 - i);
        int d2 = (soma * 10) % 11;
        if (d2 == 10 || d2 == 11) d2 = 0;
        return d2 == Character.getNumericValue(cpf.charAt(10));
    }
}