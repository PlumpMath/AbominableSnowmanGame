package backend;

import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

import javax.imageio.ImageIO;

/**
 * @author Benjamin
 *
 * TODO: Comment me.
 */
public class ImageIDTuple implements Serializable {

    /**
     * TODO: Comment me.
     */
    private static final long serialVersionUID = 4306173524148123898L;

    /**
     * TODO: Comment me.
     */
    public transient BufferedImage image;
    
    /**
     * TODO: Comment me.
     */
    public Integer ID;
    
    /**
     * TODO: Comment me.
     * 
     * @param image
     * @param ID
     */
    public ImageIDTuple(BufferedImage image, int ID) {
        this.image = image;
        this.ID = ID;
    }
    
    private void writeObject(ObjectOutputStream out) throws IOException {
        out.defaultWriteObject();
        ImageIO.write(image, "png", out);
    }

    private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
        in.defaultReadObject();
        image = ImageIO.read(in);
    }

}
