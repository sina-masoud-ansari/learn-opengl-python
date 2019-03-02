from OpenGL.GL import *
from ctypes import *
import glm

class Shader():

    def __init__(self, vertex_path, fragment_path):

        # vertex shader
        with open(vertex_path, 'r') as f:
            self.vertex_shader = glCreateShader(GL_VERTEX_SHADER)
            glShaderSource(self.vertex_shader, f.read())
            glCompileShader(self.vertex_shader)
            if glGetShaderiv(self.vertex_shader, GL_COMPILE_STATUS) != GL_TRUE:
                raise RuntimeError(glGetShaderInfoLog(self.vertex_shader))

        # fragment shader
        with open(fragment_path, 'r') as f:
            self.fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
            glShaderSource(self.fragment_shader, f.read())
            glCompileShader(self.fragment_shader)
            if glGetShaderiv(self.fragment_shader, GL_COMPILE_STATUS) != GL_TRUE:
                raise RuntimeError(glGetShaderInfoLog(self.fragment_shader))

        self.program = glCreateProgram()
        glAttachShader(self.program, self.vertex_shader)
        glAttachShader(self.program, self.fragment_shader)
        glLinkProgram(self.program)

        if glGetProgramiv(self.program, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(self.program))

        glDeleteShader(self.vertex_shader)
        glDeleteShader(self.fragment_shader)

    def get_uniform_location(self, name):
        return glGetUniformLocation(self.program, name)

    def use(self):
        glUseProgram(self.program)

    def set_bool(self, name, value):
        self.set_int(name, value)

    def set_int(self, name, value):
        glUniform1i(self.get_uniform_location(name), c_int32(value))

    def set_float(self, name, value=0):
        glUniform1f(self.get_uniform_location(name), c_float(value))

    def set_float3(self, name, v0=0., v1=0., v2=0.):
        glUniform3f(self.get_uniform_location(name), c_float(v0), c_float(v1), c_float(v2))

    def set_mat4(self, name, value, count=1, transpose=GL_FALSE):
        glUniformMatrix4fv(self.get_uniform_location(name), count, transpose, glm.value_ptr(value))