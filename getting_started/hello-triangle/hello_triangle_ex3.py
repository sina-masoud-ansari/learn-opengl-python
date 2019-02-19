from glfw import *
from OpenGL.GL import *
import numpy as np

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


    fragment_shader_a_source = """
    #version 330 core
    out vec4 FragColor;

    void main()
    {
        FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
    }

    """
    fragment_shader_a = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader_a, fragment_shader_a_source)
    glCompileShader(fragment_shader_a)
    if glGetShaderiv(fragment_shader_a, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(fragment_shader_a))

    fragment_shader_b_source = """
    #version 330 core
    out vec4 FragColor;

    void main()
    {
        FragColor = vec4(1.0f, 1.0f, 0.2f, 1.0f);
    }

    """
    fragment_shader_b = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader_b, fragment_shader_b_source)
    glCompileShader(fragment_shader_b)
    if glGetShaderiv(fragment_shader_b, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(fragment_shader_b))


    shader_program_a = glCreateProgram()
    glAttachShader(shader_program_a, vertex_shader)
    glAttachShader(shader_program_a, fragment_shader_a)
    glLinkProgram(shader_program_a)

    if glGetProgramiv(shader_program_a, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(shader_program_a))

    glDeleteShader(fragment_shader_a)

    shader_program_b = glCreateProgram()
    glAttachShader(shader_program_b, vertex_shader)
    glAttachShader(shader_program_b, fragment_shader_b)
    glLinkProgram(shader_program_b)

    if glGetProgramiv(shader_program_b, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(shader_program_b))

    glDeleteShader(fragment_shader_b)
    glDeleteShader(vertex_shader)


    vertices_a = np.array([
                        # triangle a
                        -1, -1, 0,
                        -1, 0, 0,
                        0, -1, 0,
                        ], dtype=np.float32)

    vertices_b = np.array([
                        # triangle b
                        0, -1, 0,
                        1, 0, 0,
                        1, -1, 0
                        ], dtype=np.float32)


    # generate buffers
    VAO_a, VAO_b = glGenVertexArrays(2)
    VBO_a, VBO_b = glGenBuffers(2)

    # vertex array buffer
    glBindVertexArray(VAO_a)

    # vertex buffer a
    glBindBuffer(GL_ARRAY_BUFFER, VBO_a)
    glBufferData(GL_ARRAY_BUFFER, vertices_a.nbytes, vertices_a, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * np.dtype(np.float32).itemsize, None)
    glEnableVertexAttribArray(0)


    # vertex array buffer
    glBindVertexArray(VAO_b)

    # vertex buffer b
    glBindBuffer(GL_ARRAY_BUFFER, VBO_b)
    glBufferData(GL_ARRAY_BUFFER, vertices_b.nbytes, vertices_b, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * np.dtype(np.float32).itemsize, None)
    glEnableVertexAttribArray(0)

    # unbind buffer and vertex array objects
    glBindVertexArray(0)



    # Loop until the user closes the window
    while not window_should_close(window):
        # Render here, e.g. using pyOpenGL
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader_program_a)
        glBindVertexArray(VAO_a)
        glDrawArrays(GL_TRIANGLES, 0, 9)

        glUseProgram(shader_program_b)
        glBindVertexArray(VAO_b)
        glDrawArrays(GL_TRIANGLES, 0, 9)


        glBindVertexArray(0)

        # Swap front and back buffers
        swap_buffers(window)

        # Poll for and process events
        poll_events()

    glDeleteVertexArrays(1, VAO_a)
    glDeleteVertexArrays(1, VAO_b)
    glDeleteBuffers(1, VBO_a)
    glDeleteBuffers(1, VBO_b)

    terminate()

if __name__ == "__main__":
    main()