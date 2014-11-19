package backend;

import java.io.File;

public class SceneryTypeFactory {

    public static void propogate(File input) {
        // FIXME: This should read in SceneryTypes from an XML file.
        new SceneryType("Rock");
        new SceneryType("Tree");
        new SceneryType("Cave");
    }
    
}
