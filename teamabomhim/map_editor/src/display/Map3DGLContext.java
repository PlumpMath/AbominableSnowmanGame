package display;

import org.lwjgl.LWJGLException;
import org.lwjgl.opengl.AWTGLCanvas;
import org.lwjgl.opengl.GL11;
import org.lwjgl.util.glu.GLU;

/**
 * @author Benjamin Sladewski
 * 
 * TODO: Comment me.
 */
public class Map3DGLContext extends AWTGLCanvas {

    /**
     * TODO: Comment me.
     */
    private static final long serialVersionUID = -945081470411207515L;

    /**
     * TODO: Comment me.
     * 
     * @throws LWJGLException
     */
    public Map3DGLContext() throws LWJGLException {
        super();
    }

    /**
     * TODO: Comment me.
     */
    private int height;

    /**
     * TODO: Comment me.
     */
    private int width;

    /* (non-Javadoc)
     * @see org.lwjgl.opengl.AWTGLCanvas#paintGL()
     */
    @Override
    public void paintGL() {

        try {
            if (getParent().getWidth() != width || getParent().getHeight() != height) {
                width = getParent().getWidth();
                height = getParent().getHeight();
                GL11.glViewport(0, 0, width, height);
            }
            GL11.glViewport(0, 0, getParent().getWidth(), getParent().getHeight());
            GL11.glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
            GL11.glClear(GL11.GL_COLOR_BUFFER_BIT);
            GL11.glMatrixMode(GL11.GL_PROJECTION);
            GL11.glLoadIdentity();
            GLU.gluOrtho2D(0.0f, (float) getParent().getWidth(), 0.0f, (float) getParent().getHeight());
            GL11.glMatrixMode(GL11.GL_MODELVIEW);
            GL11.glPushMatrix();
            GL11.glColor3f(1f, 1f, 1f);
            GL11.glRectf(10.0f, 10.0f, 100.0f, 100.0f);
            GL11.glPopMatrix();
            swapBuffers();
            repaint();
        } catch (LWJGLException e) {
            throw new RuntimeException(e);
        }
    }

}
