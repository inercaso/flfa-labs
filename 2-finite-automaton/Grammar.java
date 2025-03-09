package finite.automata;
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
        if (VT.contains(symbol) || symbol == 'ε') {
            System.out.println("Terminal Symbol Found: " + symbol);
            return symbol == 'ε' ? "" : symbol.toString();
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

        Set<String> Q = new HashSet<>(); // States
        for (Character nonTerminal : VN) {
            Q.add(nonTerminal.toString());
        }
        Q.add("qf"); // Add final state
        System.out.println("States (Q): " + Q);

        Set<Character> Sigma = new HashSet<>(VT); // Alphabet
        System.out.println("Alphabet (Sigma): " + Sigma);

        Map<String, Map<Character, Set<String>>> delta = new HashMap<>(); // Transition function
        String q0 = S.toString(); // Initial state
        Set<String> F = new HashSet<>(Collections.singletonList("qf")); // Final states
        System.out.println("Initial State (q0): " + q0);
        System.out.println("Final States (F): " + F);

        // Build the transition function
        for (Map.Entry<Character, List<String>> entry : P.entrySet()) {
            String fromState = entry.getKey().toString();
            for (String production : entry.getValue()) {
                if (production.equals("ε")) {
                    // Empty string means this is a final state
                    F.add(fromState);
                } else if (production.length() == 1 && VT.contains(production.charAt(0))) {
                    // Transition to final state
                    delta.computeIfAbsent(fromState, k -> new HashMap<>())
                            .computeIfAbsent(production.charAt(0), k -> new HashSet<>())
                            .add("qf");
                    System.out.println("Adding Transition: δ(" + fromState + ", " + production.charAt(0) + ") = qf");
                } else if (production.length() > 1) {
                    // Transition to next state (assuming regular grammar format: a terminal followed by a non-terminal)
                    char terminal = production.charAt(0);
                    char nonTerminal = production.charAt(1);
                    if (VT.contains(terminal) && VN.contains(nonTerminal)) {
                        delta.computeIfAbsent(fromState, k -> new HashMap<>())
                                .computeIfAbsent(terminal, k -> new HashSet<>())
                                .add(String.valueOf(nonTerminal));
                        System.out.println("Adding Transition: δ(" + fromState + ", " + terminal + ") = " + nonTerminal);
                    }
                }
            }
        }

        System.out.println("Transition Function (Delta): " + delta);
        System.out.println("=== End Of Conversion ===\n");
        return new FiniteAutomaton(Q, Sigma, delta, q0, F);
    }

    // Classify grammar according to Chomsky hierarchy
    public String classifyGrammar() {
        System.out.println("\n=== Classifying Grammar According to Chomsky Hierarchy ===");

        boolean isType0 = true; // Type 0: Unrestricted Grammar (default)
        boolean isType1 = true; // Type 1: Context-Sensitive Grammar
        boolean isType2 = true; // Type 2: Context-Free Grammar
        boolean isType3 = true; // Type 3: Regular Grammar

        // Check each production rule
        for (Map.Entry<Character, List<String>> entry : P.entrySet()) {
            Character nonTerminal = entry.getKey();
            for (String production : entry.getValue()) {

                // Check for empty string production (allowed in Type 2 and Type 3)
                if (production.equals("ε")) {
                    if (nonTerminal != S) {
                        isType3 = false; // Regular grammars only allow ε from start symbol
                    }
                    continue;
                }

                // Type 1: Context-Sensitive Grammar (|α| ≤ |β| for each production α → β)
                if (1 > production.length()) {
                    isType1 = false;
                    isType2 = false;
                    isType3 = false;
                }

                // Type 2: Context-Free Grammar (A → α, where A is a single non-terminal)
                // Already satisfied by our grammar format

                // Type 3: Regular Grammar (A → aB or A → a, where A,B are non-terminals and a is terminal)
                if (production.length() > 1) {
                    // Check if first symbol is terminal
                    char firstChar = production.charAt(0);

                    if (!VT.contains(firstChar)) {
                        isType3 = false;
                    }

                    // Check subsequent symbols (if any)
                    for (int i = 1; i < production.length(); i++) {
                        char currentChar = production.charAt(i);

                        // For Type 3, only the last symbol can be non-terminal
                        if (i < production.length() - 1 && VN.contains(currentChar)) {
                            isType3 = false;
                        }

                        // Last symbol must be non-terminal in Type 3
                        if (i == production.length() - 1 && !VN.contains(currentChar)) {
                            isType3 = false;
                        }
                    }
                }
            }
        }

        String result;
        if (isType3) {
            result = "Type 3: Regular Grammar";
        } else if (isType2) {
            result = "Type 2: Context-Free Grammar";
        } else if (isType1) {
            result = "Type 1: Context-Sensitive Grammar";
        } else {
            result = "Type 0: Unrestricted Grammar";
        }

        System.out.println("Classification: " + result);
        System.out.println("=== End Of Classification ===\n");
        return result;
    }
}