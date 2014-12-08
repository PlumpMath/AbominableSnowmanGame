package backend;

import org.lwjgl.util.vector.Vector3f;

/**
 * @author Benjamin
 *
 * TODO: Comment me.
 */
public class Triangle {

    // TODO: Comment me.
    public VertexColorPosition p0, p1, p2;
    
    public Vector3f normal;
    
    /**
     * TODO: Comment me.
     * 
     * @param p0
     * @param p1
     * @param p2
     */
    public Triangle(VertexColorPosition p0, VertexColorPosition p1,
                    VertexColorPosition p2) {
        this.p0 = p0;
        this.p1 = p1;
        this.p2 = p2;
        calcNormal();
    }
    
    public void calcNormal() {
        normal = new Vector3f();
        Vector3f calU = new Vector3f(p1.x-p0.x, p1.y-p0.y, p1.z-p0.z);
        Vector3f calV = new Vector3f(p2.x-p0.x, p2.y-p0.y, p2.z-p0.z);
        normal = new Vector3f();
        normal.x = calU.y*calV.z - calU.z*calV.y;
        normal.y = calU.z*calV.x - calU.x*calV.z;
        normal.z = calU.x*calV.y - calU.y*calV.x;
    }

}
