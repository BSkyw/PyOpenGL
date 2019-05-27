
import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from PIL import Image

rectangleVertex = [
    -0.5, -0.5,
    0.5, -0.5,
    0.5, 0.5,
    -0.5,0.5
]
diamondVertex = [
    -0.5,0.0,
    0.0,-1.0,
    0.5,0.0,
    0.0,1.0
]

quadTexture =[

    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,
]

cubeVertex = [
     - 1, -1, 1,
     1, -1, 1,
     -1, 1, 1,
     1, 1, 1,


    - 1, -1, -1,
    1, -1, -1,
    -1, 1, -1,
    1, 1, -1,


    - 1, -1, -1,
    -1, -1, 1,
    -1, 1, -1,
    -1, 1, 1,


    1, -1, -1,
    1, -1, 1,
    1, 1, -1,
    1, 1, 1,


    1, 1, -1,
    -1, 1, -1,
    1, 1, 1,
    -1, 1, 1,

    1, -1, -1,
    -1, -1, -1,
    1, -1, 1,
    -1, -1, 1,

]

# The basic Vertex shader
kDefaultVertexShader = '''
//basicV
attribute vec2 TexCoordIn;
attribute vec3 position;
varying vec2 TexCoordOut;
void main()
{
    gl_Position = vec4( position.x,position.y,position.z,1.0);

    TexCoordOut = TexCoordIn;
}
'''
# The basic Fragment shader
kDefaultFragmentShader = '''
//basicF
varying vec2 TexCoordOut;
uniform sampler2D Texture;

void main()
{
    gl_FragColor = texture2D(Texture, TexCoordOut);
}
'''

def getTex(imgName):

    image = Image.open(imgName).transpose(Image.FLIP_TOP_BOTTOM)
    width2 = image.size[0]
    height2 = image.size[1]
    print("input image w=%d,h=%d" % (image.size[0], image.size[1],))
    image = image.crop((0, 0, width2, height2))
    image = image.convert("RGBA")
    byteImage = np.array(list(image.getdata()), np.uint8)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    # setup texture
    texIndex = glGenTextures(1)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texIndex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width2, height2, 0, GL_RGBA, GL_UNSIGNED_BYTE,byteImage)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glGenerateMipmap(GL_TEXTURE_2D)
    # make the texture the default
    glBindTexture(GL_TEXTURE_2D, 0)

    return width2, height2, texIndex
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
a = 0.01
def drawTriangle(program):

    glClearColor(1.0,1.0,0.0,1.0)
    w, h, a = getTex('temp.jpg')
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, 512, 512)
    glUseProgram(program)
    p = glGetAttribLocation(program, "position")
    c = glGetAttribLocation(program, "TexCoordIn")
    t = glGetUniformLocation(program, "Texture")

    rectangleVertex[0]+=a
    time.sleep(0.1)
    glEnableVertexAttribArray(p)
    glVertexAttribPointer(p,
                          3,
                          GL_FLOAT,
                          GL_FALSE,
                          0,
                          cubeVertex)
    glEnableVertexAttribArray(c)
    glVertexAttribPointer(c,
                          2,
                          GL_FLOAT,
                          GL_FALSE,
                          0,
                          quadTexture)

    glActiveTexture(GL_TEXTURE0)  # 激活0号纹理单元，一定要使用glActiveTexture(GL_TEXTURE0), 千万不要使用glActiveTexture(0)
    glBindTexture(GL_TEXTURE_2D, a)
    glUniform1i(t, 0)

    glDrawArrays(GL_TRIANGLE_FAN, 0, 24)    #GL_TRIANGLE_FAN 头尾相连  GL_TRIANGLE_STRIP 头尾不相连

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








