import java.util.*;

public class FiniteAutomaton {
    private final Set<Character> Q; // States
    private final Set<Character> Sigma; // Alphabet
    private final Map<Character, Map<Character, Character>> delta; // Transition function
    private final Character q0; // Initial state
    private final Set<Character> F; // Final states

    public FiniteAutomaton(Set<Character> Q, Set<Character> Sigma, Map<Character, Map<Character, Character>> delta, Character q0, Set<Character> F) {
        this.Q = Q;
        this.Sigma = Sigma;
        this.delta = delta;
        this.q0 = q0;
        this.F = F;
    }

    // Check if the input string belongs to the language
    public boolean stringBelongToLanguage(final String inputString) {
        System.out.println("\n=== Checking String: '" + inputString + "' ===");

        Character currentState = q0;
        System.out.println("Starting At State: " + currentState);

        for (char c : inputString.toCharArray()) {
            if (!delta.containsKey(currentState)) {
                System.out.println("No Transitions Found From State: " + currentState);
                System.out.println("=== String Does Not Belong To Language ===\n");
                return false;
            }

            Map<Character, Character> transitions = delta.get(currentState);
            if (!transitions.containsKey(c)) {
                System.out.println("No Transition Found For Symbol '" + c + "' From State: " + currentState);
                System.out.println("=== String Does Not Belong To Language ===\n");
                return false;
            }

            currentState = transitions.get(c);
            System.out.println("Moved To State: " + currentState + " On Symbol: " + c);
        }

        boolean isFinalState = F.contains(currentState);
        System.out.println("Ended At State: " + currentState + " (Final State: " + isFinalState + ")");
        System.out.println("=== String Belongs To Language: " + isFinalState + " ===\n");
        return isFinalState;
    }
}