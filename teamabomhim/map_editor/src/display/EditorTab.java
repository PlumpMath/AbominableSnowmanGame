package display;

import java.awt.BorderLayout;
import java.awt.Graphics;
import java.io.Serializable;

import javax.swing.JPanel;

import backend.Color;
import backend.ImageIDTuple;

/**
 * @author Benjamin Sladewski
 *
 * TODO: Comment me.
 */
public class EditorTab extends JPanel implements Serializable {

    /**
     * TODO: Comment me.
     */
    private static final long serialVersionUID = 6975209371549778480L;

    /**
     * TODO: Comment me.
     */
    private EditorCanvas editorCanvas;
    
    private String displayName;
    
    private Integer ID;

    /**
     * TODO: Comment me.
     * 
     * @param width
     * @param height
     */
    public EditorTab(int width, int height, String displayName,
                     EditorCanvas.MapType mt, Color mc) {
        ID = displayName.hashCode();
        setLayout(new BorderLayout());
        setDisplayName(displayName);
        editorCanvas = new EditorCanvas(width, height, ID, mt, mc);
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
    
    public void setDisplayName(String displayName) {
        this.displayName = displayName;
    }
    
    public String getDisplayName() {
        return displayName;
    }

    /**
     * TODO: Comment me.
     *
     * @return
     */
    public Integer getID() {
        return ID;
    }
    
    public ImageIDTuple getImageTuple() {
        return editorCanvas.getImageTuple();
    }

    /* (non-Javadoc)
     * @see javax.swing.JComponent#paintComponent(java.awt.Graphics)
     */
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
    }

    /**
     * TODO: Comment me.
     * 
     * @param it
     */
    public void swapImageTuple(ImageIDTuple it) {
        editorCanvas.swapImageTuple(it);
    }

}
