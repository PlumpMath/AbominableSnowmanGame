package backend;

import java.util.ArrayList;

/**
 * @author Benjamin Sladewski
 * @version 2014-11-19
 * @since 2014-11-19
 *
 * this class represents a type of scenery in the team Abominable Snowman of the
 * Himilayas map editor.
 */
public class SceneryType {

    /**
     * all scenery that currently exists.
     */
    private static ArrayList<SceneryType> currentTypes;

    // instantiates the static list of types.
    static {
        setCurrentTypes(new ArrayList<SceneryType>());
    }

    /**
     * the name to display in the application.
     */
    private String name;

    /**
     * @param name the name to display in the application.
     */
    public SceneryType(String name) {
        currentTypes.add(this);
        setName(name);
    }

    /**
     * gets the name of this scenery type.
     * 
     * @return the name to display in the application.
     */
    public String getName() {
        return name;
    }

    /**
     * sets the name of this scenery type.
     * 
     * @param name the name to display in the application.
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * gets the list of all scenery that currently exists.
     * 
     * @return the list of all scenery that currently exists.
     */
    public static ArrayList<SceneryType> getCurrentTypes() {
        return currentTypes;
    }

    /**
     * sets the list of all scenery that currently exists.
     * 
     * @param currentTypes the list of all scenery that currently exists.
     */
    public static void setCurrentTypes(ArrayList<SceneryType> currentTypes) {
        SceneryType.currentTypes = currentTypes;
    }

    /* (non-Javadoc)
     * @see java.lang.Object#toString()
     */
    public String toString() {
        return name;
    }

}
