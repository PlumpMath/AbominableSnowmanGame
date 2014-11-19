package display;

import javax.swing.JPanel;
import net.miginfocom.swing.MigLayout;
import javax.swing.JTabbedPane;
import java.awt.Cursor;

/**
 * @author Benjamin Sladewski
 * @version 2014-11-19
 * @since 2014-11-19
 *
 * this class represents a 2D map for editing maps in the team Abominable
 * Snowman of the Himilayas map editor.
 */
public class Map2D extends JPanel {

    /**
     * the unique ID for the Map2D class.
     */
    private static final long serialVersionUID = -6095943892036919371L;

    /**
     * constructs a new 2D Map for editing maps.
     */
    public Map2D() {
        // TODO: Comment me
        setCursor(Cursor.getPredefinedCursor(Cursor.CROSSHAIR_CURSOR));
        setLayout(new MigLayout("", "[grow]", "[grow]"));
        
        // TODO: Comment me
        JTabbedPane tabbedPane = new JTabbedPane(JTabbedPane.TOP);
        add(tabbedPane, "cell 0 0,grow");
    }

}
