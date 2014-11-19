package display;

import javax.swing.JPanel;
import java.awt.Color;

/**
 * @author Benjamin Sladewski
 * @version 2014-11-19
 * @since 2014-11-19
 *
 * this class represents a 3D map for rendering the map being edited by the
 * team Abominable Snowman of the Himilayas map editor.
 */
public class Map3D extends JPanel {

    /**
     * the unique ID for the Map3D class.
     */
    private static final long serialVersionUID = -8801621936985706128L;

    /**
     * constructs a new 3D Map for rendering the current map.
     */
    public Map3D() {
        // TODO: Comment me
        setBackground(Color.BLACK);
    }

}
