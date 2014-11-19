package display;

import java.awt.Component;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.EventQueue;

import javax.swing.Box;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JToolBar;
import javax.swing.UIManager;
import javax.swing.border.EmptyBorder;
import javax.swing.border.TitledBorder;

import net.miginfocom.swing.MigLayout;
import backend.SceneryTypeFactory;

/**
 * @author Benjamin Sladewski
 * @version 2014-11-19
 * @since 2014-11-19
 *
 * this class is the main application for the team Abominable Snowman of the
 * Himalayas map editor.
 */
public class MapEditor extends JFrame {

    /**
     * the unique ID for the MapEditor class.
     */
    private static final long serialVersionUID = 1088013217014844618L;

    /**
     * the panel that contains the components of the application.
     */
    private JPanel contentPane;

    /**
     * launches the application.
     */
    public static void main(String[] args) {
        // FIXME: this should pass in an XML file holding the scenery
        //        definition.
        SceneryTypeFactory.propogate(null);
        EventQueue.invokeLater(new Runnable() {
            public void run() {
                try {
                    MapEditor frame = new MapEditor();
                    frame.setVisible(true);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
    }

    /**
     * constructs a new JFrame with the components of the map editor.
     */
    public MapEditor() {
        // TODO: Comment me
        setMinimumSize(new Dimension(800, 600));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setBounds(100, 100, 700, 492);
        contentPane = new JPanel();
        contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
        setContentPane(contentPane);
        contentPane.setLayout(new MigLayout("", "[grow][grow]", "[][][grow]"));
        
        // TODO: Comment me
        JToolBar toolBar = new JToolBar();
        toolBar.setBorder(UIManager.getBorder("ToolBar.border"));
        contentPane.add(toolBar, "flowx,cell 0 0 2 1,growx");
        
        // TODO: Comment me
        JButton btnSave = new JButton("");
        btnSave.setIcon(new ImageIcon("res/save.png"));
        btnSave.setToolTipText("Save");
        btnSave.setBorder(null);
        toolBar.add(btnSave);
        
        // TODO: Comment me
        Component horizontalStrut = Box.createHorizontalStrut(20);
        horizontalStrut.setMaximumSize(new Dimension(5, 32767));
        horizontalStrut.setPreferredSize(new Dimension(5, 0));
        horizontalStrut.setMinimumSize(new Dimension(5, 0));
        toolBar.add(horizontalStrut);
        
        // TODO: Comment me
        JButton btnLoad = new JButton("");
        btnLoad.setBorder(null);
        btnLoad.setToolTipText("Load");
        btnLoad.setIcon(new ImageIcon("res/load.png"));
        toolBar.add(btnLoad);
        
        // TODO: Comment me
        Component horizontalStrut_1 = Box.createHorizontalStrut(20);
        toolBar.add(horizontalStrut_1);
        
        // TODO: Comment me
        JButton btnExport = new JButton("");
        btnExport.setBorder(null);
        btnExport.setIcon(new ImageIcon("res/export.png"));
        btnExport.setToolTipText("Export");
        toolBar.add(btnExport);
        
        // TODO: Comment me
        Component horizontalStrut_2 = Box.createHorizontalStrut(20);
        toolBar.add(horizontalStrut_2);
        
        // TODO: Comment me
        JButton btnUndo = new JButton("");
        btnUndo.setBorder(null);
        btnUndo.setToolTipText("Undo");
        btnUndo.setIcon(new ImageIcon("res/undo.png"));
        toolBar.add(btnUndo);
        
        // TODO: Comment me
        Component horizontalStrut_3 = Box.createHorizontalStrut(20);
        horizontalStrut_3.setPreferredSize(new Dimension(5, 0));
        horizontalStrut_3.setMinimumSize(new Dimension(5, 0));
        horizontalStrut_3.setMaximumSize(new Dimension(5, 32767));
        toolBar.add(horizontalStrut_3);
        
        // TODO: Comment me
        JButton btnRedo = new JButton("");
        btnRedo.setBorder(null);
        btnRedo.setIcon(new ImageIcon("res/redo.png"));
        btnRedo.setToolTipText("Redo");
        toolBar.add(btnRedo);

        // TODO: Comment me
        JPanel toolboxPanel = new JPanel();
        toolboxPanel.setBackground(UIManager.getColor("Panel.background"));
        contentPane.add(toolboxPanel, "cell 0 1 2 1,grow");
        toolboxPanel.setLayout(new MigLayout("", "[666px,grow]", "[122px]"));
        Toolbox toolbox = new Toolbox();
        toolboxPanel.add(toolbox, "cell 0 0,growx,aligny top");

        // TODO: Comment me
        JPanel map2dPanel = new JPanel();
        map2dPanel.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
        map2dPanel.setBorder(new TitledBorder(null, "2D Map",
                             TitledBorder.LEADING, TitledBorder.TOP, null,
                             null));
        map2dPanel.setBackground(UIManager.getColor("Panel.background"));
        map2dPanel.setLayout(new MigLayout("", "[19px,grow,fill]",
                             "[19px,grow,fill]"));
        map2dPanel.add(new Map2D(), "cell 0 0,alignx left,aligny top");
        contentPane.add(map2dPanel, "cell 0 2,grow");

        // TODO: Comment me
        JPanel map3dPanel = new JPanel();
        map3dPanel.setBorder(new TitledBorder(null, "3D Map",
                             TitledBorder.LEADING, TitledBorder.TOP, null,
                             null));
        map3dPanel.setBackground(UIManager.getColor("Panel.background"));
        map3dPanel.setLayout(new MigLayout("", "[10px,grow]", "[10px,grow]"));
        map3dPanel.add(new Map3D(), "cell 0 0,grow");
        contentPane.add(map3dPanel, "cell 1 2,grow");
    }

}
