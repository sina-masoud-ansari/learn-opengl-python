from glfw import *
from OpenGL.GL import *
import numpy as np
from ctypes import *

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
    vertex_shader_source = """
    #version 330 core
    layout (location = 0) in vec3 aPos;

    void main()
    {
        gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0f);
    }

    """
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_source)
    glCompileShader(vertex_shader)
    if glGetShaderiv(vertex_shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(vertex_shader))


    fragment_shader_source = """
    #version 330 core
    out vec4 FragColor;

    void main()
    {
        FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
    }

    """
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_source)
    glCompileShader(fragment_shader)
    if glGetShaderiv(fragment_shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(fragment_shader))


    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    if glGetProgramiv(shader_program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(shader_program))

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    vertices = np.array([
                         0.5,  0.5, 0.0,  # top right
                         0.5, -0.5, 0.0,  # bottom right
                        -0.5, -0.5, 0.0,  # bottom left
                        -0.5,  0.5, 0.0   # top left
                        ], dtype=np.float32)

    indices = np.array([
                        0, 1, 3,
                        1, 2, 3
                       ],dtype=np.uint32)


    # generate buffers
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    # vertex array buffer
    glBindVertexArray(VAO)

    # vertex buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # element array buffer
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(c_float), c_void_p(0))
    glEnableVertexAttribArray(0)

    # unbind buffer and vertex array objects
    glBindVertexArray(0)
    #glBindBuffer(GL_ARRAY_BUFFER, 0)
    #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)


    # Loop until the user closes the window
    while not window_should_close(window):
        # Render here, e.g. using pyOpenGL
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader_program)
        glBindVertexArray(VAO)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, c_void_p(0))
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