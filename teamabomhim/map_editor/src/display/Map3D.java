package display;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.util.ArrayList;

import javax.swing.JInternalFrame;
import javax.swing.JPanel;
import javax.swing.plaf.basic.BasicInternalFrameUI;

import net.miginfocom.swing.MigLayout;

import org.lwjgl.LWJGLException;

import backend.ImageColorTuple;
import backend.Mesh;
import backend.Triangle;
import backend.VertexColorPosition;

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
     * 
     */
    public static Map3D current;
    
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
        genMap(Map2D.mapSize);
        current = this;
    }

    ////////////////////////////////////////////////////////////////////////
    // What preceded this is the stupidest thing I have ever written     //
    ////////////////////////////////////////////////////////////////////////

    /**
     * TODO: Comment me.
     */
    public void genMap(int mapSize) {
        Mesh m = new Mesh();
        // Generate all left-hand polygons
        for(int i = 0; i < mapSize - 2; i += 2)
            for(int j = 0; j < mapSize - 2; j += 2) {
                Triangle left = new Triangle(
                            new VertexColorPosition(i, j, 0, 0.5f, 0.5f, 0.5f),
                            new VertexColorPosition(i, j + 2, 0, 0.5f, 0.5f, 0.5f),
                            new VertexColorPosition(i + 2, j, 0, 0.5f, 0.5f, 0.5f));
                Triangle right = new Triangle(
                            new VertexColorPosition(i, j + 2, 0, 0.5f, 0.5f, 0.5f),
                            new VertexColorPosition(i + 2, j + 2, 0, 0.5f, 0.5f, 0.5f),
                            new VertexColorPosition(i + 2, j, 0, 0.5f, 0.5f, 0.5f));
                m.geometry.add(left);
                m.geometry.add(right);
            }
        glCanvas.landscape = m;
        blankMap();
    }

    /**
     * TODO: Comment me.
     */
    public void blankMap() {
        blankHeight();
        blankColor();
    }

    /**
     * TODO: Comment me.
     */
    public void blankHeight() {
        for(Triangle t : glCanvas.landscape.geometry) {
            t.p0.z = 0.0f;
            t.p1.z = 0.0f;
            t.p2.z = 0.0f;
        }
    }

    /**
     * TODO: Comment me.
     */
    public void blankColor() {
        for(Triangle t : glCanvas.landscape.geometry) {
            t.p0.r = 0.5f;
            t.p0.g = 0.5f;
            t.p0.b = 0.5f;
            t.p1.r = 0.5f;
            t.p1.g = 0.5f;
            t.p1.b = 0.5f;
            t.p1.r = 0.5f;
            t.p1.g = 0.5f;
            t.p1.b = 0.5f;
        }
    }

    /**
     * TODO: Comment me.
     * 
     * @param b
     */
    public void updateHeightmap(BufferedImage b) {
        for(Triangle t : glCanvas.landscape.geometry) {
            t.p0.z = new Color(b.getRGB((int) t.p0.x, (int) t.p0.y)).getRed();
            t.p1.z = new Color(b.getRGB((int) t.p1.x, (int) t.p1.y)).getRed();
            t.p2.z = new Color(b.getRGB((int) t.p2.x, (int) t.p2.y)).getRed();
            t.calcNormal();
        }
    }

    /**
     * TODO: Comment me.
     * 
     * @param icts
     */
    public void updateTexMap(ArrayList<ImageColorTuple> icts) {
        for(ImageColorTuple ict : icts) {
            for(Triangle t : glCanvas.landscape.geometry) {
                Color c = new Color(ict.b.getRGB((int) t.p0.x, (int) t.p0.y));
                if(c.getRed() > 0.0f) {
                    t.p0.r = ict.c.getRed();
                    t.p0.g = ict.c.getGreen();
                    t.p0.b = ict.c.getBlue();
                }
                c = new Color(ict.b.getRGB((int) t.p1.x, (int) t.p1.y));
                if(c.getRed() > 0.0f) {
                    t.p1.r = ict.c.getRed();
                    t.p1.g = ict.c.getGreen();
                    t.p1.b = ict.c.getBlue();
                }
                c = new Color(ict.b.getRGB((int) t.p2.x, (int) t.p2.y));
                if(c.getRed() > 0.0f) {
                    t.p2.r = ict.c.getRed();
                    t.p2.g = ict.c.getGreen();
                    t.p2.b = ict.c.getBlue();
                }
            }
        }
    }
}
