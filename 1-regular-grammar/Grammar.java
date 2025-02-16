import java.util.*;

public class Grammar {
    private final Set<Character> VN; // Non-terminal symbols
    private final Set<Character> VT; // Terminal symbols
    private final Map<Character, List<String>> P; // Production rules
    private final Character S; // Start symbol

    public Grammar(Set<Character> VN, Set<Character> VT, Map<Character, List<String>> P, Character S) {
        this.VN = VN;
        this.VT = VT;
        this.P = P;
        this.S = S;
    }

    // Generate a valid string from the grammar
    public String generateString() {
        System.out.println("\n=== Starting String Generation ===");
        String result = generateStringHelper(S);
        System.out.println("Generated String: " + result);
        System.out.println("=== End Of String Generation ===\n");
        return result;
    }

    private String generateStringHelper(Character symbol) {
        if (VT.contains(symbol)) {
            System.out.println("Terminal Symbol Found: " + symbol);
            return symbol.toString();
        }

        List<String> productions = P.get(symbol);
        if (productions == null || productions.isEmpty()) {
            System.out.println("No Productions Found For Symbol: " + symbol);
            return "";
        }

        // Randomly select a production
        String production = productions.get(new Random().nextInt(productions.size()));
        System.out.println("Applying Production For Symbol " + symbol + ": " + symbol + " → " + production);

        StringBuilder result = new StringBuilder();
        for (char c : production.toCharArray()) {
            result.append(generateStringHelper(c));
        }

        return result.toString();
    }

    // Convert the grammar to a finite automaton
    public FiniteAutomaton toFiniteAutomaton() {
        System.out.println("\n=== Converting Grammar To Finite Automaton ===");

        Set<Character> Q = new HashSet<>(VN); // States
        Q.add('F'); // Add an additional final state
        System.out.println("States (Q): " + Q);

        Set<Character> Sigma = new HashSet<>(VT); // Alphabet
        System.out.println("Alphabet (Sigma): " + Sigma);

        Map<Character, Map<Character, Character>> delta = new HashMap<>(); // Transition function
        Character q0 = S; // Initial state
        Set<Character> F = new HashSet<>(Collections.singletonList('F')); // Final states
        System.out.println("Initial State (q0): " + q0);
        System.out.println("Final States (F): " + F);

        // Build the transition function
        for (Map.Entry<Character, List<String>> entry : P.entrySet()) {
            Character fromState = entry.getKey();
            for (String production : entry.getValue()) {
                if (production.length() == 1 && VT.contains(production.charAt(0))) {
                    // Transition to final state
                    delta.computeIfAbsent(fromState, k -> new HashMap<>())
                            .put(production.charAt(0), 'F');
                    System.out.println("Adding Transition: δ(" + fromState + ", " + production.charAt(0) + ") = F");
                } else if (production.length() > 1) {
                    // Transition to next state
                    delta.computeIfAbsent(fromState, k -> new HashMap<>())
                            .put(production.charAt(0), production.charAt(1));
                    System.out.println("Adding Transition: δ(" + fromState + ", " + production.charAt(0) + ") = " + production.charAt(1));
                }
            }
        }

        System.out.println("Transition Function (Delta): " + delta);
        System.out.println("=== End Of Conversion ===\n");
        return new FiniteAutomaton(Q, Sigma, delta, q0, F);
    }
}