package finite.automata;

import org.jgrapht.Graph;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.ext.JGraphXAdapter;
import com.mxgraph.layout.mxCircleLayout;
import com.mxgraph.swing.mxGraphComponent;
import com.mxgraph.util.mxConstants;

import javax.swing.*;
import java.util.Map;
import java.util.Set;

public class AutomatonVisualizer {

    private final Set<String> states; // States of the automaton
    private final Set<Character> alphabet; // Alphabet of the automaton
    private final Map<String, Map<Character, Set<String>>> transitions; // Transition function
    private final String initialState; // Initial state
    private final Set<String> finalStates; // Final states

    public AutomatonVisualizer(Set<String> states, Set<Character> alphabet,
                               Map<String, Map<Character, Set<String>>> transitions,
                               String initialState, Set<String> finalStates) {
        this.states = states;
        this.alphabet = alphabet;
        this.transitions = transitions;
        this.initialState = initialState;
        this.finalStates = finalStates;
    }

    public void visualize() {
        // Create a directed graph
        Graph<String, DefaultEdge> graph = new DefaultDirectedGraph<>(DefaultEdge.class);

        // Add states as vertices
        for (String state : states) {
            graph.addVertex(state);
        }

        // Add transitions as edges
        for (String state : states) {
            if (transitions.containsKey(state)) {
                for (Map.Entry<Character, Set<String>> entry : transitions.get(state).entrySet()) {
                    char symbol = entry.getKey();
                    for (String nextState : entry.getValue()) {
                        graph.addEdge(state, nextState);
                    }
                }
            }
        }

        // Visualize the graph using JGraphX
        JGraphXAdapter<String, DefaultEdge> graphAdapter = new JGraphXAdapter<>(graph);

        // Customize the appearance of states and edges
        graphAdapter.getStylesheet().getDefaultVertexStyle().put(mxConstants.STYLE_SHAPE, mxConstants.SHAPE_ELLIPSE);
        graphAdapter.getStylesheet().getDefaultVertexStyle().put(mxConstants.STYLE_FILLCOLOR, "#FFFFFF"); // White background
        graphAdapter.getStylesheet().getDefaultVertexStyle().put(mxConstants.STYLE_STROKECOLOR, "#000000"); // Black border

        // Highlight final states with double circles
        for (String state : finalStates) {
            Object cell = graphAdapter.getVertexToCellMap().get(state);
            graphAdapter.setCellStyle(mxConstants.STYLE_SHAPE + "=" + mxConstants.SHAPE_DOUBLE_ELLIPSE, new Object[]{cell});
        }

        // Apply a layout (e.g., circular layout)
        mxCircleLayout layout = new mxCircleLayout(graphAdapter);
        layout.execute(graphAdapter.getDefaultParent());

        // Create a JFrame to display the graph
        JFrame frame = new JFrame("Finite Automaton Visualization");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Add the graph to the frame
        mxGraphComponent graphComponent = new mxGraphComponent(graphAdapter);
        frame.getContentPane().add(graphComponent);

        // Display the frame
        frame.pack();
        frame.setLocationRelativeTo(null); // Center the window
        frame.setVisible(true);
    }
}