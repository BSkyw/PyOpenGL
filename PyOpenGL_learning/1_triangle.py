from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

triangleVertex=[
    -0.5, -0.5,
    0.5, -0.5,
    0.0, 0.5
]

# The basic Vertex shader
kDefaultVertexShader = '''
//basicV
attribute vec2 position;
void main()
{
    gl_Position = vec4(position,1.0,1.0);

}
'''
# The basic Fragment shader
kDefaultFragmentShader = '''
uniform sampler2D Texture;

void main()
{
    gl_FragColor = vec4(1.0,0.0,0.0,1.0);//texture2D(Texture, TexCoordOut);
}
'''

def InitProgram(vertexShader, fragShader):
    program = glCreateProgram()
    vertex = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    # Set shaders source
    glShaderSource(vertex, vertexShader)
    glShaderSource(fragment, fragShader)

    # Compile shaders
    glCompileShader(vertex)
    glCompileShader(fragment)

    fragSuccess = glGetShaderiv(fragment, GL_COMPILE_STATUS)
    vertSuccess = glGetShaderiv(vertex, GL_COMPILE_STATUS)
    print("%s vertext shader compile  success  [%s]" % (vertexShader[0:8], vertSuccess,))
    print("%s fragment shader compile  success  [%s]" % (fragShader[0:8], fragSuccess,))

    if vertSuccess == 0:
        print(glGetShaderInfoLog(vertex))
        sys.exit(0)

    if fragSuccess == 0:
        print(glGetShaderInfoLog(fragment))
        sys.exit(0)

    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)
    linksucc = glGetProgramiv(program, GL_LINK_STATUS)
    print("link  program success [%s]" % (linksucc,))
    return program

def drawTriangle(program):

    glClearColor(1.0,1.0,0.0,1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, 512, 512)
    glUseProgram(program)
    p = glGetAttribLocation(program, "position")

    glEnableVertexAttribArray(p)
    glVertexAttribPointer(p,
                          2,
                          GL_FLOAT,
                          GL_FALSE,
                          0,
                          triangleVertex)

    glDrawArrays(GL_TRIANGLE_STRIP, 0, 3)

    glutSwapBuffers()

# 使用glut初始化OpenGL
glutInit()
# 显示模式:GLUT_SINGLE无缓冲直接显示|GLUT_RGBA采用RGB(A非alpha)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
# 窗口位置及大小-生成
glutInitWindowPosition(0 ,0)
glutInitWindowSize(512 ,512)
glutCreateWindow("Style Show")
# 调用函数绘制图像
program = InitProgram(kDefaultVertexShader,kDefaultFragmentShader)
glutDisplayFunc(drawTriangle)
glutIdleFunc(drawTriangle(program))
# 主循环
glutMainLoop()








