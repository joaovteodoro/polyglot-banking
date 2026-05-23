package model;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

public class Banco {

    private final List<Usuario> usuarios = new ArrayList<>();
    private final List<Conta>   contas   = new ArrayList<>();

    public Optional<Usuario> buscarUsuario(String cpf) {
        String cpfLimpo = cpf.replaceAll("\\D", "");
        return usuarios.stream()
                       .filter(u -> u.getCpf().equals(cpfLimpo))
                       .findFirst();
    }

    public boolean cadastrarUsuario(String cpf, String nome,
                                    String dataDeNascimento, Endereco endereco) {
        if (buscarUsuario(cpf).isPresent()) return false;
        usuarios.add(new Usuario(cpf, nome, dataDeNascimento, endereco));
        return true;
    }

    public Optional<Conta> cadastrarConta(String cpf) {
        return buscarUsuario(cpf).map(usuario -> {
            Conta nova = new Conta(contas.size() + 1, usuario);
            contas.add(nova);
            return nova;
        });
    }

    public List<Conta> filtrarContas(String cpf) {
        String cpfLimpo = cpf.replaceAll("\\D", "");
        return contas.stream()
                     .filter(c -> c.getCpf().equals(cpfLimpo))
                     .toList();
    }

    public Optional<Conta> buscarConta(String cpf, int numeroConta) {
        return filtrarContas(cpf).stream()
                                 .filter(c -> c.getNumeroConta() == numeroConta)
                                 .findFirst();
    }

    public List<Conta> getContas() {
        return Collections.unmodifiableList(contas);
    }
}