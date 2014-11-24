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
    
    private float rotx = 0.0f, roty = 0.0f, rotz = 0.0f;

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
            GLU.gluPerspective(45.0f, (float) getParent().getWidth() / (float) getParent().getHeight(), 0.1f, 1000.0f);
            GL11.glMatrixMode(GL11.GL_MODELVIEW);
            GL11.glPushMatrix();
                // Top of Cube
                GL11.glTranslatef(0.0f, 0.0f, -5.0f);
                GL11.glRotatef(rotx, 1.0f, 0.0f, 0.0f);
                GL11.glRotatef(roty, 0.0f, 1.0f, 0.0f);
                GL11.glRotatef(rotz, 0.0f, 0.0f, 1.0f);
                GL11.glBegin(GL11.GL_TRIANGLES);
                    GL11.glColor3f(1.0f,0.0f,0.0f);     
                    GL11.glVertex3f( 0.0f, 1.0f, 0.0f); 
                    GL11.glColor3f(0.0f,1.0f,0.0f);     
                    GL11.glVertex3f(-1.0f,-1.0f, 1.0f); 
                    GL11.glColor3f(0.0f,0.0f,1.0f);     
                    GL11.glVertex3f( 1.0f,-1.0f, 1.0f);
                    
                    GL11.glColor3f(1.0f,0.0f,0.0f);     
                    GL11.glVertex3f( 0.0f, 1.0f, 0.0f); 
                    GL11.glColor3f(0.0f,0.0f,1.0f);     
                    GL11.glVertex3f( 1.0f,-1.0f, 1.0f); 
                    GL11.glColor3f(0.0f,1.0f,0.0f);     
                    GL11.glVertex3f( 1.0f,-1.0f, -1.0f);
                    
                    GL11.glColor3f(1.0f,0.0f,0.0f);     
                    GL11.glVertex3f( 0.0f, 1.0f, 0.0f); 
                    GL11.glColor3f(0.0f,1.0f,0.0f);     
                    GL11.glVertex3f( 1.0f,-1.0f, -1.0f);
                    GL11.glColor3f(0.0f,0.0f,1.0f);     
                    GL11.glVertex3f(-1.0f,-1.0f, -1.0f);
                    
                    GL11.glColor3f(1.0f,0.0f,0.0f);    
                    GL11.glVertex3f( 0.0f, 1.0f, 0.0f);
                    GL11.glColor3f(0.0f,0.0f,1.0f);    
                    GL11.glVertex3f(-1.0f,-1.0f,-1.0f);
                    GL11.glColor3f(0.0f,1.0f,0.0f);    
                    GL11.glVertex3f(-1.0f,-1.0f, 1.0f);
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
                rotx += 0.5f;
                roty += 0.5f;
                rotz += 0.5f;
                Thread.sleep(16);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

}
