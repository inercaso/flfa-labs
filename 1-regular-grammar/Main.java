package regular.grammar;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        // Define the grammar components
        Set<Character> VN = new HashSet<>(Arrays.asList('S', 'D', 'E', 'F', 'L'));
        Set<Character> VT = new HashSet<>(Arrays.asList('a', 'b', 'c', 'd'));
        Map<Character, List<String>> P = new HashMap<>();
        P.put('S', Arrays.asList("aD"));
        P.put('D', Arrays.asList("bE"));
        P.put('E', Arrays.asList("cF", "dL"));
        P.put('F', Arrays.asList("dD"));
        P.put('L', Arrays.asList("aL", "bL", "c"));
        Character S = 'S';

        // Create the grammar
        System.out.println("=== Creating Grammar ===");
        Grammar grammar = new Grammar(VN, VT, P, S);

        // Generate 5 valid strings
        System.out.println("\n=== Generating 5 Valid Strings ===");
        for (int i = 0; i < 5; i++) {
            System.out.println("String " + (i + 1) + ":");
            grammar.generateString();
        }

        // Convert the grammar to a finite automaton
        System.out.println("\n=== Converting Grammar To Finite Automaton ===");
        FiniteAutomaton automaton = grammar.toFiniteAutomaton();

        // Check if some strings belong to the language
        String[] testStrings = {"abcd", "abdc", "abc", "adc", "abbbbc"};
        System.out.println("\n=== Checking Strings ===");
        for (String testString : testStrings) {
            System.out.println("Testing String: " + testString);
            boolean belongs = automaton.stringBelongToLanguage(testString);
            System.out.println("Result: " + (belongs ? "Belongs" : "Does Not Belong"));
        }
    }
}