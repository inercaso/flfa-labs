package finite.automata;
import java.util.*;

public class FiniteAutomaton {
    private final Set<String> Q; // States
    private final Set<Character> Sigma; // Alphabet
    private final Map<String, Map<Character, Set<String>>> delta; // Transition function (NDFA ready)
    private final String q0; // Initial state
    private final Set<String> F; // Final states

    public FiniteAutomaton(Set<String> Q, Set<Character> Sigma, Map<String, Map<Character, Set<String>>> delta, String q0, Set<String> F) {
        this.Q = Q;
        this.Sigma = Sigma;
        this.delta = delta;
        this.q0 = q0;
        this.F = F;
    }

    // Check if the input string belongs to the language (for both DFA and NDFA)
    public boolean stringBelongToLanguage(final String inputString) {
        System.out.println("\n=== Checking String: '" + inputString + "' ===");

        // For NDFA we need to track multiple states
        Set<String> currentStates = new HashSet<>();
        currentStates.add(q0);
        System.out.println("Starting At State(s): " + currentStates);
        for (char c : inputString.toCharArray()) {
            Set<String> nextStates = new HashSet<>();

            for (String state : currentStates) {
                if (delta.containsKey(state) && delta.get(state).containsKey(c)) {
                    nextStates.addAll(delta.get(state).get(c));
                }
            }

            if (nextStates.isEmpty()) {
                System.out.println("No Transitions Found For Symbol '" + c + "' From States: " + currentStates);
                System.out.println("=== String Does Not Belong To Language ===\n");
                return false;
            }

            currentStates = nextStates;
            System.out.println("Moved To State(s): " + currentStates + " On Symbol: " + c);
        }

        // Check if any of the current states is a final state
        boolean hasReachedFinalState = false;
        for (String state : currentStates) {
            if (F.contains(state)) {
                hasReachedFinalState = true;
                break;
            }
        }

        System.out.println("Ended At State(s): " + currentStates);
        System.out.println("=== String Belongs To Language: " + hasReachedFinalState + " ===\n");
        return hasReachedFinalState;
    }

    // Determine if the automaton is deterministic
    public boolean isDeterministic() {
        System.out.println("\n=== Checking if Automaton is Deterministic ===");

        for (String state : Q) {
            if (!delta.containsKey(state)) {
                continue; // No transitions from this state
            }

            Map<Character, Set<String>> stateTransitions = delta.get(state);

            for (char symbol : Sigma) {
                if (stateTransitions.containsKey(symbol)) {
                    Set<String> nextStates = stateTransitions.get(symbol);
                    if (nextStates.size() > 1) {
                        System.out.println("Multiple transitions found from state " + state +
                                " with symbol " + symbol + " to states " + nextStates);
                        System.out.println("=== Automaton is Non-Deterministic ===\n");
                        return false;
                    }
                }
            }
        }

        // Also check that each state has exactly one transition for each symbol
        for (String state : Q) {
            if (!delta.containsKey(state)) {
                // For a complete DFA, each state must have transitions for all symbols
                System.out.println("State " + state + " has no outgoing transitions");
                System.out.println("=== Automaton is Non-Deterministic (or incomplete) ===\n");
                return false;
            }

            Set<Character> definedSymbols = delta.get(state).keySet();
            if (!definedSymbols.equals(Sigma)) {
                System.out.println("State " + state + " doesn't have transitions for all symbols in the alphabet");
                System.out.println("=== Automaton is Non-Deterministic (or incomplete) ===\n");
                return false;
            }
        }

        System.out.println("=== Automaton is Deterministic ===\n");
        return true;
    }

    // Convert NDFA to DFA
    public FiniteAutomaton toDFA() {
        System.out.println("\n=== Converting NDFA to DFA ===");

        // Create new states and transitions
        Set<String> dfaQ = new HashSet<>(); // DFA states (sets of NDFA states)
        Map<String, Map<Character, Set<String>>> dfaDelta = new HashMap<>();
        Set<String> dfaF = new HashSet<>(); // DFA final states

        // Start with the initial state
        Set<String> initialStateSet = new HashSet<>();
        initialStateSet.add(q0);
        String initialState = setToState(initialStateSet);

        // Queue for states to process
        Queue<Set<String>> queue = new LinkedList<>();
        queue.add(initialStateSet);

        // Set to keep track of processed state sets
        Set<Set<String>> processedStateSets = new HashSet<>();

        while (!queue.isEmpty()) {
            Set<String> currentStateSet = queue.poll();

            if (processedStateSets.contains(currentStateSet)) {
                continue;
            }

            processedStateSets.add(currentStateSet);
            String currentDFAState = setToState(currentStateSet);
            dfaQ.add(currentDFAState);

            // Check if this composite state contains any final states
            for (String state : currentStateSet) {
                if (F.contains(state)) {
                    dfaF.add(currentDFAState);
                    break;
                }
            }

            // Process transitions for each symbol
            for (char symbol : Sigma) {
                Set<String> nextStateSet = new HashSet<>();

                // Find all reachable states from current state set
                for (String state : currentStateSet) {
                    if (delta.containsKey(state) && delta.get(state).containsKey(symbol)) {
                        nextStateSet.addAll(delta.get(state).get(symbol));
                    }
                }

                if (!nextStateSet.isEmpty()) {
                    String nextDFAState = setToState(nextStateSet);

                    // Add transition to DFA
                    dfaDelta.computeIfAbsent(currentDFAState, k -> new HashMap<>())
                            .computeIfAbsent(symbol, k -> new HashSet<>())
                            .add(nextDFAState);

                    // Add next state set to the queue for processing
                    if (!processedStateSets.contains(nextStateSet)) {
                        queue.add(nextStateSet);
                    }
                }
            }
        }

        System.out.println("DFA States: " + dfaQ);
        System.out.println("DFA Transitions: " + dfaDelta);
        System.out.println("DFA Initial State: " + initialState);
        System.out.println("DFA Final States: " + dfaF);
        System.out.println("=== Conversion Complete ===\n");

        return new FiniteAutomaton(dfaQ, Sigma, dfaDelta, initialState, dfaF);
    }

    // Helper method to convert a set of states to a single DFA state name
    private String setToState(Set<String> stateSet) {
        if (stateSet.isEmpty()) {
            return "{}";
        }
        List<String> sortedStates = new ArrayList<>(stateSet);
        Collections.sort(sortedStates);
        return sortedStates.toString();
    }

    // Convert finite automaton to regular grammar
    public Grammar toRegularGrammar() {
        System.out.println("\n=== Converting Finite Automaton to Regular Grammar ===");

        // Create grammar components
        Set<Character> VN = new HashSet<>(); // Non-terminal symbols
        Set<Character> VT = new HashSet<>(Sigma); // Terminal symbols
        Map<Character, List<String>> P = new HashMap<>(); // Production rules
        Character S; // Start symbol

        // Map automaton states to non-terminal symbols
        Map<String, Character> stateToNonTerminal = new HashMap<>();
        char nonTerminalChar = 'S';

        for (String state : Q) {
            stateToNonTerminal.put(state, nonTerminalChar);
            VN.add(nonTerminalChar);
            nonTerminalChar++;
        }

        // Start symbol corresponds to initial state
        S = stateToNonTerminal.get(q0);

        // Create production rules
        for (String state : Q) {
            Character nonTerminal = stateToNonTerminal.get(state);
            List<String> productions = new ArrayList<>();

            if (delta.containsKey(state)) {
                for (Map.Entry<Character, Set<String>> entry : delta.get(state).entrySet()) {
                    char symbol = entry.getKey();
                    for (String nextState : entry.getValue()) {
                        if (F.contains(nextState)) {
                            // If next state is final, add production with just terminal
                            productions.add(String.valueOf(symbol));
                        } else {
                            // Otherwise, add production with terminal followed by non-terminal
                            productions.add(symbol + String.valueOf(stateToNonTerminal.get(nextState)));
                        }
                    }
                }
            }

            // Add empty string production for final states
            if (F.contains(state)) {
                productions.add("ε");
            }

            P.put(nonTerminal, productions);
        }

        System.out.println("Grammar Non-terminals (VN): " + VN);
        System.out.println("Grammar Terminals (VT): " + VT);
        System.out.println("Grammar Productions (P): " + P);
        System.out.println("Grammar Start Symbol (S): " + S);
        System.out.println("=== Conversion Complete ===\n");

        return new Grammar(VN, VT, P, S);
    }

    // Print the finite automaton definition
    public void printAutomaton() {
        System.out.println("\n=== Finite Automaton Definition ===");
        System.out.println("States (Q): " + Q);
        System.out.println("Alphabet (Sigma): " + Sigma);
        System.out.println("Initial State (q0): " + q0);
        System.out.println("Final States (F): " + F);
        System.out.println("Transition Function (Delta):");

        for (String state : Q) {
            if (delta.containsKey(state)) {
                for (Map.Entry<Character, Set<String>> entry : delta.get(state).entrySet()) {
                    char symbol = entry.getKey();
                    Set<String> nextStates = entry.getValue();
                    System.out.println("δ(" + state + ", " + symbol + ") = " + nextStates);
                }
            }
        }

        System.out.println("=== End of Definition ===\n");
    }
}