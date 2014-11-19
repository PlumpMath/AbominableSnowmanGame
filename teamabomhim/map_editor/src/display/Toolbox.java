package display;

import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JSlider;
import javax.swing.border.TitledBorder;

import net.miginfocom.swing.MigLayout;
import backend.SceneryType;

/**
 * @author Benjamin Sladewski
 * @version 2014-11-19
 * @since 2014-11-19
 *
 * this class allows users to select tools and modify options in the team
 * Abominable Snowman of the Himalayas map editor.
 */
public class Toolbox extends JPanel {

    /**
     * the unique ID for the Toolbox class.
     */
    private static final long serialVersionUID = -4637733821926927993L;

    /**
     * constructs a new toolbox.
     */
    public Toolbox() {
        setLayout(new MigLayout("", "[][grow][grow]", "[]"));

        // TODO: Comment me.
        JPanel panel = new JPanel();
        panel.setBorder(new TitledBorder(null, "Tools", TitledBorder.LEADING,
                        TitledBorder.TOP, null, null));
        add(panel, "cell 0 0,grow");
        panel.setLayout(new MigLayout("", "[grow][][]", "[][]"));

        // TODO: Comment me.
        JRadioButton rdbtnPencil = new JRadioButton("");
        rdbtnPencil.setToolTipText("Pencil");
        rdbtnPencil.setSelected(true);
        rdbtnPencil.setSelectedIcon(new ImageIcon("res/pencils.png"));
        rdbtnPencil.setIcon(new ImageIcon("res/pencil.png"));
        panel.add(rdbtnPencil, "cell 0 0");

        // TODO: Comment me.
        JRadioButton rdbtnBrush = new JRadioButton("");
        rdbtnBrush.setToolTipText("Brush");
        rdbtnBrush.setIcon(new ImageIcon("res/brush.png"));
        rdbtnBrush.setSelectedIcon(new ImageIcon("res/brushs.png"));
        panel.add(rdbtnBrush, "cell 1 0");

        // TODO: Comment me.
        JRadioButton rdbtnCloud = new JRadioButton("");
        rdbtnCloud.setToolTipText("Cloud");
        rdbtnCloud.setIcon(new ImageIcon("res/cloud.png"));
        rdbtnCloud.setSelectedIcon(new ImageIcon("res/clouds.png"));
        panel.add(rdbtnCloud, "cell 2 0");

        // TODO: Comment me.
        JComboBox<SceneryType> cmbxScenery = new JComboBox<SceneryType>();
        for(SceneryType s : SceneryType.getCurrentTypes())
            cmbxScenery.addItem(s);
        panel.add(cmbxScenery, "cell 0 1 2 1,growx");

        // TODO: Comment me.
        JRadioButton rdbtnScenery = new JRadioButton("");
        rdbtnScenery.setToolTipText("Scenery");
        rdbtnScenery.setIcon(new ImageIcon("res/scenery.png"));
        rdbtnScenery.setSelectedIcon(new ImageIcon("res/scenerys.png"));
        panel.add(rdbtnScenery, "cell 2 1");

        // TODO: Comment me.
        ButtonGroup tools = new ButtonGroup();
        tools.add(rdbtnPencil);
        tools.add(rdbtnBrush);
        tools.add(rdbtnCloud);
        tools.add(rdbtnScenery);

        // TODO: Comment me.
        JPanel panel_1 = new JPanel();
        panel_1.setBorder(new TitledBorder(null, "Tool Options",
                          TitledBorder.LEADING, TitledBorder.TOP, null, null));
        add(panel_1, "cell 1 0,grow");
        panel_1.setLayout(new MigLayout("", "[][grow]", "[][]"));

        // TODO: Comment me.
        JLabel lblSize = new JLabel("Size");
        panel_1.add(lblSize, "cell 0 0");

        // TODO: Comment me.
        JSlider sliderSize = new JSlider();
        sliderSize.setPaintLabels(true);
        sliderSize.setPaintTicks(true);
        sliderSize.setSnapToTicks(true);
        sliderSize.setMajorTickSpacing(10);
        sliderSize.setMinorTickSpacing(2);
        panel_1.add(sliderSize, "cell 1 0,growx");

        // TODO: Comment me.
        JLabel lblOpacity = new JLabel("Opacity");
        panel_1.add(lblOpacity, "cell 0 1");

        // TODO: Comment me.
        JSlider sliderOpacity = new JSlider();
        sliderOpacity.setValue(100);
        sliderOpacity.setMajorTickSpacing(10);
        sliderOpacity.setMinorTickSpacing(2);
        sliderOpacity.setSnapToTicks(true);
        sliderOpacity.setPaintTicks(true);
        sliderOpacity.setPaintLabels(true);
        panel_1.add(sliderOpacity, "cell 1 1,growx");

        // TODO: Comment me.
        JPanel panel_2 = new JPanel();
        panel_2.setBorder(new TitledBorder(null, "3D Options",
                          TitledBorder.LEADING, TitledBorder.TOP, null, null));
        add(panel_2, "cell 2 0,grow");
        panel_2.setLayout(new MigLayout("", "[][grow]", "[]"));

        // TODO: Comment me.
        JLabel lblZoom = new JLabel("Zoom");
        panel_2.add(lblZoom, "cell 0 0");

        // TODO: Comment me.
        JSlider sliderZoom = new JSlider();
        sliderZoom.setValue(0);
        sliderZoom.setSnapToTicks(true);
        sliderZoom.setPaintTicks(true);
        sliderZoom.setPaintLabels(true);
        sliderZoom.setMinorTickSpacing(2);
        sliderZoom.setMajorTickSpacing(10);
        panel_2.add(sliderZoom, "cell 1 0,growx");
    }

}
