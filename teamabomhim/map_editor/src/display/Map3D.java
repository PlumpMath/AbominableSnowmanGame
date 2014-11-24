package display;

import javax.swing.JInternalFrame;
import javax.swing.JPanel;
import javax.swing.plaf.basic.BasicInternalFrameUI;

import net.miginfocom.swing.MigLayout;

import org.lwjgl.LWJGLException;

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
     * TODO: Comment me.
     */
    private Map3DGLContext glCanvas;

    ////////////////////////////////////////////////////////////////////////
    // What follows is the stupidest thing I have ever written.           //
    ////////////////////////////////////////////////////////////////////////

    /**
     * constructs a new 3D Map for rendering the current map.
     * @throws LWJGLException 
     */
    public Map3D() throws LWJGLException {
        setLayout(new MigLayout("", "[grow]", "[grow]"));
        JInternalFrame mapContainer = new JInternalFrame();
        mapContainer.setResizable(false);
        mapContainer.remove(((BasicInternalFrameUI)
                            mapContainer.getUI()).getNorthPane());
        mapContainer.setBorder(null);
        glCanvas = new Map3DGLContext();
        Thread glThread = new Thread(glCanvas);
        glThread.start();
        mapContainer.getContentPane().add(glCanvas);
        mapContainer.setVisible(true);
        add(mapContainer, "cell 0 0,grow");
    }

    ////////////////////////////////////////////////////////////////////////
    // What preceded this is the stupidest thing I have ever written     //
    ////////////////////////////////////////////////////////////////////////

}
