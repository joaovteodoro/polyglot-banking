import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Banco  banco   = new Banco();
        Scanner scanner = new Scanner(System.in);
        new MenuUI(banco, scanner).iniciar();
        scanner.close();
    }
}