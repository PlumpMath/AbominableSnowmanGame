package backend;

import java.io.File;

/**
 * @author Benjamin Sladewski
 * 
 * TODO: Comment me.
 */
public class SceneryTypeFactory {

    /**
     * TODO: Comment me.
     * 
     * @param input
     */
    public static void propogate(File input) {
        // FIXME: This should read in SceneryTypes from an XML file.
        new SceneryType("Rock");
        new SceneryType("Tree");
        new SceneryType("Cave");
    }

}
