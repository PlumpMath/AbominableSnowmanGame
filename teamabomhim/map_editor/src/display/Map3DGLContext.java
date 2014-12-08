package display;

import org.lwjgl.LWJGLException;
import org.lwjgl.opengl.AWTGLCanvas;
import org.lwjgl.opengl.GL11;
import org.lwjgl.util.glu.GLU;

import backend.Mesh;
import backend.Triangle;

/**
 * @author Benjamin Sladewski
 * 
 * TODO: Comment me.
 */
public class Map3DGLContext extends AWTGLCanvas implements Runnable {

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

    /**
     * TODO: Comment me.
     */
    public Mesh landscape;

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
            GL11.glViewport(0, 0, getParent().getWidth(),
                                  getParent().getHeight());
            GL11.glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
            GL11.glClear(GL11.GL_COLOR_BUFFER_BIT);
            GL11.glMatrixMode(GL11.GL_PROJECTION);
            GL11.glLoadIdentity();
            GLU.gluPerspective(45.0f, (float) getParent().getWidth()
                               / (float) getParent().getHeight(), 0.1f,
                               2000.0f);
            GL11.glMatrixMode(GL11.GL_MODELVIEW);
            GL11.glPushMatrix();
                GL11.glTranslatef(-Map2D.mapSize / 2, -Map2D.mapSize / 2,
                                  -Map2D.mapSize * 1.5f);
                GL11.glRotatef(-60.0f , 1.0f, 0.0f, 0.0f);

                GL11.glBegin(GL11.GL_TRIANGLES);
                    if(landscape != null)
                        for(Triangle t : landscape.geometry) {
                            //
                            GL11.glNormal3f(t.normal.x, t.normal.y, t.normal.z);
                            //
                            GL11.glColor3f(t.p0.r, t.p0.g, t.p0.b);
                            GL11.glVertex3f(t.p0.x, t.p0.y, t.p0.z);
                            GL11.glColor3f(t.p1.r, t.p1.g, t.p1.b);
                            GL11.glVertex3f(t.p1.x, t.p1.y, t.p1.z);
                            GL11.glColor3f(t.p2.r, t.p2.g, t.p2.b);
                            GL11.glVertex3f(t.p2.x, t.p2.y, t.p2.z);
                        }
                GL11.glEnd();
            GL11.glPopMatrix();
            swapBuffers();
            repaint();
        } catch (LWJGLException e) {
            throw new RuntimeException(e);
        }
    }

    /* (non-Javadoc)
     * @see java.lang.Runnable#run()
     */
    @Override
    public void run() {
        while(true) {
            try {
                Thread.sleep(16);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

}
