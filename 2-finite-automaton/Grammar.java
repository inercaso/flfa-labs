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

        // Separate checks for each grammar type
        boolean isType0 = true; // All grammars are at least Type 0
        boolean isType1 = checkType1Grammar(); // |α| ≤ |β|
        boolean isType2 = isType1 && checkType2Grammar(); // A ∈ V (single non-terminal on left)
        boolean isType3 = isType2 && checkType3Grammar(); // A → aB or A → a

        // Check if grammar is derived from an automaton
        boolean isAutomatonDerived = checkIfAutomatonDerived();

        // For a grammar derived from an automaton, it should be Type 3
        if (isAutomatonDerived) {
            isType3 = true;
            System.out.println("Grammar is derived from finite automaton - classified as Type 3");
        }

        // Determine the most specific grammar type
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

    // Type 0: Unrestricted Grammar - α → β where α ≠ NULL (contains at least one non-terminal)
    private boolean checkType0Grammar() {
        // All our grammars are at least Type 0 because we use a map with non-terminal keys
        return true;
    }

    // Type 1: Context-Sensitive Grammar - |α| ≤ |β|
    // Exception: S → ε is allowed if S doesn't appear on the right side of any production
    private boolean checkType1Grammar() {
        boolean hasEpsilonRule = false;
        boolean sAppearsOnRightSide = false;

        // First check if S appears on any right-hand side
        for (List<String> productions : P.values()) {
            for (String production : productions) {
                if (production.indexOf(S) >= 0) {
                    sAppearsOnRightSide = true;
                    break;
                }
            }
            if (sAppearsOnRightSide) break;
        }

        // Check all productions
        for (Map.Entry<Character, List<String>> entry : P.entrySet()) {
            Character leftSide = entry.getKey(); // Single non-terminal

            for (String rightSide : entry.getValue()) {
                // Check for epsilon rule
                if (rightSide.equals("ε")) {
                    if (leftSide == S && !sAppearsOnRightSide) {
                        // This is the S → ε exception case
                        continue;
                    } else {
                        return false; // Not Type 1
                    }
                }

                // For Type 1, |α| ≤ |β| must hold for all productions
                // In our case, |α| is always 1 (single non-terminal)
                if (rightSide.length() < 1) {
                    return false; // Not Type 1 because |β| < |α|
                }
            }
        }

        return true;
    }

    // Type 2: Context-Free Grammar - A ∈ V (left side is a single non-terminal)
    private boolean checkType2Grammar() {
        // This is automatically satisfied by our grammar representation
        // which only allows single non-terminals on the left side
        return true;
    }

    // Type 3: Regular Grammar - A → aB or A → a
    private boolean checkType3Grammar() {
        for (Map.Entry<Character, List<String>> entry : P.entrySet()) {
            for (String production : entry.getValue()) {
                // Allow ε production
                if (production.equals("ε")) {
                    continue;
                }

                // Check for A → a (single terminal)
                if (production.length() == 1) {
                    if (!VT.contains(production.charAt(0))) {
                        return false; // Not of form A → a
                    }
                }
                // Check for A → aB (terminal followed by non-terminal)
                else if (production.length() == 2) {
                    if (!VT.contains(production.charAt(0)) || !VN.contains(production.charAt(1))) {
                        return false; // Not of form A → aB
                    }
                }
                // Any other form means this is not Type 3
                else {
                    return false;
                }
            }
        }

        return true;
    }

    // Check if grammar appears to be derived from a finite automaton
    private boolean checkIfAutomatonDerived() {
        // A grammar derived from an automaton should be Type 3 (regular)
        // So first check if it's regular
        if (!checkType3Grammar()) {
            return false;
        }

        // Additionally, check for characteristic patterns of automaton-derived grammars:
        // 1. Each non-terminal typically represents a state
        // 2. Productions represent transitions between states

        // For simplicity, we'll assume that if it's a regular grammar
        // with consistent structure, it's automaton-derived

        return true;
    }
}