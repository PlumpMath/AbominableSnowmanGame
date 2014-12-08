package display;

import java.awt.Cursor;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.HashMap;

import javax.swing.JFileChooser;
import javax.swing.JPanel;
import javax.swing.JTabbedPane;
import javax.swing.SwingUtilities;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.filechooser.FileNameExtensionFilter;

import net.miginfocom.swing.MigLayout;
import backend.Color;
import backend.ImageIDTuple;

/**
 * @author Benjamin Sladewski
 * @version 2014-11-19
 * @since 2014-11-19
 *
 * this class represents a 2D map for editing maps in the team Abominable
 * Snowman of the Himalayas map editor.
 */
public class Map2D extends JPanel {

    /**
     * the unique ID for the Map2D class.
     */
    private static final long serialVersionUID = -6095943892036919371L;
    
    public static int mapSize;
    
    private HashMap<Integer, EditorTab> id2Tab;

    /**
     * TODO: Comment me.
     */
    private JTabbedPane tabbedPane;

    /**
     * constructs a new 2D Map for editing maps.
     */
    public Map2D() {
        // TODO: Comment me
        id2Tab = new HashMap<Integer, EditorTab>();
        setCursor(Cursor.getPredefinedCursor(Cursor.CROSSHAIR_CURSOR));
        setLayout(new MigLayout("", "[grow]", "[grow]"));
        
        // TODO: Comment me
        tabbedPane = new JTabbedPane(JTabbedPane.TOP);
        tabbedPane.addChangeListener(new ChangeListener() {
            
            @Override
            public void stateChanged(ChangeEvent arg0) {
                MapEditor.currentTab =
                        (EditorTab) tabbedPane.getSelectedComponent();
            }
        });
        add(tabbedPane, "cell 0 0,grow");
        
        // FIXME: generate tabs from XML file.
        mapSize = 512;
        EditorTab[] tabs = {new EditorTab(mapSize, mapSize, "Heightmap",
                                          EditorCanvas.MapType.HEIGHT,
                                          new Color(0.0f, 0.0f, 0.0f)),
                            new EditorTab(mapSize, mapSize, "Icemap",
                                          EditorCanvas.MapType.TEXTURE,
                                          new Color(0.5f, 0.5f, 1.0f)),
                            new EditorTab(mapSize, mapSize, "Snowmap",
                                          EditorCanvas.MapType.TEXTURE,
                                          new Color(1.0f, 1.0f, 1.0f)),
                            new EditorTab(mapSize, mapSize, "Scenerymap",
                                          EditorCanvas.MapType.SCENERY,
                                          new Color(0, 0, 0))};
        id2Tab.put(tabs[0].getID(), tabs[0]);
        id2Tab.put(tabs[1].getID(), tabs[1]);
        id2Tab.put(tabs[2].getID(), tabs[2]);
        id2Tab.put(tabs[3].getID(), tabs[3]);
        
        for(EditorTab e : id2Tab.values())
            tabbedPane.addTab(e.getDisplayName(), e);
        MapEditor.currentTab = (EditorTab) tabbedPane.getSelectedComponent();
    }

    /**
     * TODO: Comment me.
     */
    public void save() {
        JFileChooser fc = new JFileChooser();
        FileNameExtensionFilter ef =
                new FileNameExtensionFilter("MapEditor Save File", "sav");
        fc.setFileFilter(ef);
        int retVal = fc.showOpenDialog(SwingUtilities.getWindowAncestor(this));
        if(retVal == JFileChooser.APPROVE_OPTION) {
            File f = new File(fc.getSelectedFile() + ".sav");
            FileOutputStream fout = null;
            ObjectOutputStream oout = null;
            try {
                fout = new FileOutputStream(f);
                oout = new ObjectOutputStream(fout);
                ArrayList<ImageIDTuple> aout = new ArrayList<ImageIDTuple>();
                for(EditorTab e : id2Tab.values())
                    aout.add(e.getImageTuple());
                oout.writeObject(aout);
            } catch(Exception e) {
                e.printStackTrace();
                // TODO: Error notification.
            } finally {
                try {
                    fout.close();
                    oout.close();
                } catch(Exception e) {
                    e.printStackTrace();
                    // TODO: Error handling.
                }
            }
        }
    }

    /**
     * TODO: Comment me.
     */
    @SuppressWarnings("unchecked")
    public void load() {
        JFileChooser fc = new JFileChooser();
        FileNameExtensionFilter ef =
                new FileNameExtensionFilter("MapEditor Save File", "sav");
        fc.setFileFilter(ef);
        int retVal = fc.showOpenDialog(SwingUtilities.getWindowAncestor(this));
        if(retVal == JFileChooser.APPROVE_OPTION) {
            File f = fc.getSelectedFile();
            ArrayList<ImageIDTuple> newImages = null;
            FileInputStream fin = null;
            ObjectInputStream oin = null;
            try {
                fin = new FileInputStream(f);
                oin = new ObjectInputStream(fin);
                newImages = (ArrayList<ImageIDTuple>) oin.readObject();
            } catch(Exception e) {
                e.printStackTrace();
                // TODO: Error notification.
            } finally {
                try {
                    fin.close();
                    oin.close();
                } catch(Exception e) {
                    e.printStackTrace();
                    // TODO: Error handling.
                }
            }
            if(newImages != null) {
                for(ImageIDTuple it : newImages)
                    if(id2Tab.containsKey(it.ID))
                        id2Tab.get(it.ID).swapImageTuple(it);
            }
        } else {
            // TODO: Error notification.
        }
        repaint();
    }
    
}
