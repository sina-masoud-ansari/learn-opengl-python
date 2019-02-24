from glfw import *
from OpenGL.GL import *
import numpy as np
from ctypes import *
from learnopengl import *

def resize(window, width, height):
    glViewport(0, 0, width, height)

def main():
    # Initialize the library
    if not init():
        return
    # Create a windowed mode window and its OpenGL context
    window_hint(CONTEXT_VERSION_MAJOR, 3)
    window_hint(CONTEXT_VERSION_MINOR, 3)
    window_hint(OPENGL_PROFILE, OPENGL_CORE_PROFILE)

    window = create_window(800, 600, "LearnOpenGL", None, None)
    if not window:
        terminate()

    make_context_current(window)
    set_framebuffer_size_callback(window, resize)
    glViewport(0, 0, 800, 600)

    # Make the window's context current
    make_context_current(window)

    # shaders
    shader = Shader('vertex_ex3.glsl', 'fragment.glsl')

    vertices = np.array([
                        # position      # color
                         0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                        -0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                         0.0,  0.5, 0.0, 0.0, 0.0, 1.0
                        ], dtype=np.float32)

    # generate buffers
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    # vertex array buffer
    glBindVertexArray(VAO)

    # vertex buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * np.dtype(np.float32).itemsize, c_void_p(0))
    glEnableVertexAttribArray(0)

    # color attribute
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * np.dtype(np.float32).itemsize, c_void_p(3 * np.dtype(np.float32).itemsize))
    glEnableVertexAttribArray(1)

    # unbind buffer and vertex array objects
    glBindVertexArray(0)

    shader.use()

    # Loop until the user closes the window
    while not window_should_close(window):
        # Render here, e.g. using pyOpenGL
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0)

        # Swap front and back buffers
        swap_buffers(window)

        # Poll for and process events
        poll_events()

    glDeleteVertexArrays(1, VAO)
    glDeleteBuffers(1, VBO)
    terminate()

if __name__ == "__main__":
    main()