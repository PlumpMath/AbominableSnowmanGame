package backend;

import java.util.ArrayList;

/**
 * @author Benjamin
 *
 * TODO: Comment me.
 */
public class Mesh {

    /**
     * TODO: Comment me.
     */
    public ArrayList<Triangle> geometry;

    /**
     * TODO: Comment me
     * 
     * @param geometry
     */
    public Mesh(ArrayList<Triangle> geometry) {
        this.geometry = geometry;
    }

    /**
     * TODO: Comment me.
     */
    public Mesh() {
        this(new ArrayList<Triangle>());
    }

}
