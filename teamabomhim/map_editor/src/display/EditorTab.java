package display;

import java.awt.BorderLayout;
import java.awt.Graphics;

import javax.swing.JPanel;

/**
 * @author Benjamin Sladewski
 *
 * TODO: Comment me.
 */
public class EditorTab extends JPanel {

    /**
     * TODO: Comment me.
     */
    private static final long serialVersionUID = 6975209371549778480L;

    /**
     * TODO: Comment me.
     */
    private EditorCanvas editorCanvas;

    /**
     * TODO: Comment me.
     * 
     * @param width
     * @param height
     */
    public EditorTab(int width, int height) {
        setLayout(new BorderLayout());
        editorCanvas = new EditorCanvas(width, height);
        add(editorCanvas, BorderLayout.CENTER);
    }

    /**
     * TODO: Comment me.
     * 
     * @return
     */
    public EditorCanvas getEditorCanvas() {
        return editorCanvas;
    }

    /**
     * TODO: Comment me.
     * 
     * @param editorCanvas
     */
    public void setEditorCanvas(EditorCanvas editorCanvas) {
        this.editorCanvas = editorCanvas;
    }
    
    /* (non-Javadoc)
     * @see javax.swing.JComponent#paintComponent(java.awt.Graphics)
     */
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
    }

}
