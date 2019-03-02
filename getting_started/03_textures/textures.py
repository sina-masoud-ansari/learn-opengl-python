from glfw import *
from OpenGL.GL import *
import numpy as np
from ctypes import *
from learnopengl import *
from PIL import Image


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
    shader = Shader('vertex.glsl', 'fragment.glsl')

    vertices = np.array([
             #positions        #colors          #texture coords
             0.5,  0.5, 0.0,   1.0, 0.0, 0.0,   1.0, 1.0,   # top right
             0.5, -0.5, 0.0,   0.0, 1.0, 0.0,   1.0, 0.0,   # bottom right
            -0.5, -0.5, 0.0,   0.0, 0.0, 1.0,   0.0, 0.0,   # bottom left
            -0.5,  0.5, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0    # top left
            ], dtype=np.float32)

    indices = np.array([
                0, 1, 3, # first triangle
                1, 2, 3  # second triangle
                ], dtype=np.uint32)

    image1 = Image.open('container.jpg')
    image2 = Image.open('awesomeface.png')


    # generate buffers
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)
    texture1 = glGenTextures(1)
    texture2 = glGenTextures(1)

    # vertex array buffer
    glBindVertexArray(VAO)

    # vertex buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # element buffer
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # texture1
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image1.width, image1.height, 0, GL_RGB, GL_UNSIGNED_BYTE, np.array(image1))
    glGenerateMipmap(GL_TEXTURE_2D)

    # texture1 warp
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # texture1 filter
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # texture2
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D, texture2)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image2.width, image2.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, np.flipud(np.array(image2)))
    glGenerateMipmap(GL_TEXTURE_2D)

    # texture2 warp
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # texture2 filter
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


    # position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(c_float), c_void_p(0))
    glEnableVertexAttribArray(0)

    # color attribute
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(c_float), c_void_p(3 * sizeof(c_float)))
    glEnableVertexAttribArray(1)

    # texture
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(c_float), c_void_p(6 * sizeof(c_float)))
    glEnableVertexAttribArray(2)

    # unbind buffer and vertex array objects
    glBindVertexArray(0)

    shader.use()
    shader.set_int("texture2", 1)

    # Loop until the user closes the window
    while not window_should_close(window):
        # Render here, e.g. using pyOpenGL
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # bind textures
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture1)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, texture2)

        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, c_void_p(0))
        #glBindVertexArray(0)

        # Swap front and back buffers
        swap_buffers(window)

        # Poll for and process events
        poll_events()

    glDeleteVertexArrays(1, VAO)
    glDeleteBuffers(1, VBO)
    glDeleteBuffers(1, EBO)

    terminate()

if __name__ == "__main__":
    main()