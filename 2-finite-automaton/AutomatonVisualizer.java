package finite.automata;

import org.jgrapht.Graph;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.ext.JGraphXAdapter;
import com.mxgraph.layout.mxCircleLayout;
import com.mxgraph.swing.mxGraphComponent;
import com.mxgraph.util.mxConstants;
import com.mxgraph.model.mxCell;
import com.mxgraph.view.mxStylesheet;

import javax.swing.*;
import java.util.Map;
import java.util.Set;
import java.util.HashMap;

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
        // Create a directed graph with custom edges that can hold labels
        Graph<String, LabeledEdge> graph = new DefaultDirectedGraph<>(LabeledEdge.class);

        // Add states as vertices
        for (String state : states) {
            graph.addVertex(state);
        }

        // Add transitions as labeled edges
        for (String state : states) {
            if (transitions.containsKey(state)) {
                for (Map.Entry<Character, Set<String>> entry : transitions.get(state).entrySet()) {
                    char symbol = entry.getKey();
                    for (String nextState : entry.getValue()) {
                        LabeledEdge edge = graph.addEdge(state, nextState);
                        if (edge != null) {
                            edge.setLabel(String.valueOf(symbol));
                        }
                    }
                }
            }
        }

        // Visualize the graph using JGraphX
        JGraphXAdapter<String, LabeledEdge> graphAdapter = new JGraphXAdapter<>(graph);

        // Customize the appearance of states and edges
        mxStylesheet stylesheet = graphAdapter.getStylesheet();

        // Style for vertices (states)
        Map<String, Object> vertexStyle = stylesheet.getDefaultVertexStyle();
        vertexStyle.put(mxConstants.STYLE_SHAPE, mxConstants.SHAPE_ELLIPSE);
        vertexStyle.put(mxConstants.STYLE_FILLCOLOR, "#FFFFFF"); // White background
        vertexStyle.put(mxConstants.STYLE_STROKECOLOR, "#000000"); // Black border
        vertexStyle.put(mxConstants.STYLE_FONTCOLOR, "#000000");

        // Style for edges
        Map<String, Object> edgeStyle = stylesheet.getDefaultEdgeStyle();
        edgeStyle.put(mxConstants.STYLE_LABEL_BACKGROUNDCOLOR, "#FFFFFF");
        edgeStyle.put(mxConstants.STYLE_FONTCOLOR, "#000000");
        edgeStyle.put(mxConstants.STYLE_STROKECOLOR, "#0000FF"); // Blue edges
        edgeStyle.put(mxConstants.STYLE_ENDARROW, mxConstants.ARROW_CLASSIC);

        // Highlight final states with double circles
        for (String state : finalStates) {
            Object cell = graphAdapter.getVertexToCellMap().get(state);
            graphAdapter.setCellStyle(mxConstants.STYLE_SHAPE + "=" + mxConstants.SHAPE_DOUBLE_ELLIPSE, new Object[]{cell});
        }

        // Set edge labels
        for (Object edge : graphAdapter.getChildCells(graphAdapter.getDefaultParent(), false, true)) {
            if (edge instanceof mxCell && ((mxCell) edge).isEdge()) {
                mxCell cell = (mxCell) edge;
                LabeledEdge labeledEdge = graphAdapter.getCellToEdgeMap().get(cell);
                if (labeledEdge != null) {
                    graphAdapter.cellLabelChanged(cell, labeledEdge.getLabel(), false);
                }
            }
        }

        // Apply a layout (e.g., circular layout)
        mxCircleLayout layout = new mxCircleLayout(graphAdapter);
        layout.execute(graphAdapter.getDefaultParent());

        // Create a JFrame to display the graph
        JFrame frame = new JFrame("Finite Automaton Visualization");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);

        // Add the graph to the frame
        mxGraphComponent graphComponent = new mxGraphComponent(graphAdapter);
        frame.getContentPane().add(graphComponent);

        // Display the frame
        frame.pack();
        frame.setLocationRelativeTo(null); // Center the window
        frame.setVisible(true);
    }

    // Custom edge class that can hold a label
    public static class LabeledEdge extends DefaultEdge {
        private String label;

        public LabeledEdge() {
            this.label = "";
        }

        public void setLabel(String label) {
            this.label = label;
        }

        public String getLabel() {
            return label;
        }

        @Override
        public String toString() {
            return label;
        }
    }
}