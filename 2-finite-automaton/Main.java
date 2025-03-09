package finite.automata;

import java.util.*;

public class Main {
    public static void main(String[] args) {
        // Define automaton components
        Set<String> Q = new HashSet<>(Arrays.asList("q0", "q1", "q2", "q3"));
        Set<Character> Sigma = new HashSet<>(Arrays.asList('a', 'b'));
        Map<String, Map<Character, Set<String>>> delta = new HashMap<>();
        String q0 = "q0";
        Set<String> F = new HashSet<>(Collections.singletonList("q3"));

        // Define transitions
        Map<Character, Set<String>> q0Transitions = new HashMap<>();
        q0Transitions.put('a', new HashSet<>(Collections.singletonList("q1")));
        delta.put("q0", q0Transitions);

        Map<Character, Set<String>> q1Transitions = new HashMap<>();
        q1Transitions.put('b', new HashSet<>(Collections.singletonList("q2")));
        q1Transitions.put('a', new HashSet<>(Collections.singletonList("q1")));
        delta.put("q1", q1Transitions);

        Map<Character, Set<String>> q2Transitions = new HashMap<>();
        q2Transitions.put('b', new HashSet<>(Arrays.asList("q3", "q2"))); // Non-deterministic
        delta.put("q2", q2Transitions);

        Map<Character, Set<String>> q3Transitions = new HashMap<>();
        q3Transitions.put('a', new HashSet<>(Collections.singletonList("q1")));
        delta.put("q3", q3Transitions);

        // Create the automaton
        FiniteAutomaton automaton = new FiniteAutomaton(Q, Sigma, delta, q0, F);
        automaton.printAutomaton();

        // Check if the automaton is deterministic
        boolean isDeterministic = automaton.isDeterministic();
        System.out.println("Is Deterministic: " + isDeterministic);

        // If non-deterministic, convert to DFA
        FiniteAutomaton dfa = automaton;
        if (!isDeterministic) {
            dfa = automaton.toDFA();
            dfa.printAutomaton();
        }

        // Convert the automaton to a regular grammar
        Grammar regularGrammar = automaton.toRegularGrammar();

        // Classify the grammar according to Chomsky hierarchy
        String grammarType = regularGrammar.classifyGrammar();
        System.out.println("Grammar Classification: " + grammarType);

        // Test strings with both automata
        String[] testStrings = {"a", "ab", "abb", "abba", "abbab", "abbabbabba"};

        System.out.println("\n=== Testing Strings with Original Automaton ===");
        for (String testString : testStrings) {
            boolean belongs = automaton.stringBelongToLanguage(testString);
            System.out.println("String '" + testString + "' belongs to language: " + belongs);
        }

        if (!isDeterministic) {
            System.out.println("\n=== Testing Strings with Converted DFA ===");
            for (String testString : testStrings) {
                boolean belongs = dfa.stringBelongToLanguage(testString);
                System.out.println("String '" + testString + "' belongs to language: " + belongs);
            }
        }

        // Generate strings from the regular grammar
        System.out.println("\n=== Generating Strings from Regular Grammar ===");
        for (int i = 0; i < 5; i++) {
            System.out.println("Generated String " + (i + 1) + ": " + regularGrammar.generateString());
        }

        // Visualize the automaton
        AutomatonVisualizer visualizer = new AutomatonVisualizer(Q, Sigma, delta, q0, F);
        visualizer.visualize();
    }
}