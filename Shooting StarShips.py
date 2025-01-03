import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

Window_Width, Window_Height= 500, 780
with open("score.txt") as file:
    previous_score = int(file.read())
sharp_shooter_count = 0
sharp_shooter_badge = False

stars = []
num_stars = 200

start_time = time.time()
elapsed_time = 0
survivor_badge = False

enemyCenterInitalization = random.randrange(-230, 230), 200
enemyCenter = enemyCenterInitalization
enemyColorList = [(0.5, 0.2, 0), (0.5, 0.5, 0), (0.5, 0.2, 0.5), (0, 0.7, 0.5), (0, 0.6, 0.8)]

userSpaceShipInitialPosition = 0, -190
userCurrentSpaceShipCenter = userSpaceShipInitialPosition
speed = 1
level_2_bonus, level_3_bonus, level_4_bonus, level_5_bonus, level_6_bonus, level_7_bonus = True, True, True, True, True, True

left_bullet_center = userCurrentSpaceShipCenter
right_bullet_center = userCurrentSpaceShipCenter
enemy_bullet_center = enemyCenter

score = 0
health_count = 3

background_color = 0.0, 0.0, 0.0
level_background_colors = [(0.0, 0.0, 0.0),(0.0, 0.1, 0.2),(0.3, 0.0, 0.0),(0.3, 0.0, 0.3), (0.0, 0.4, 0.5), (0.2, 0.1, 0.6), (0.2, 0.1, 0.0),]
pointSize = 2

circleSize = 2
circleColor = (0, 0.8, 1)
level = 1
crossColor = 1.0, 0.0, 0.0
backArrowColor = 0.0, 0.7, 0.8
playPauseColor = 0.0, 0.5, 0.0
userCurrentSpaceShipColor = 1.0, 1.0, 1.0
enemyColor = random.choice(enemyColorList)
# center of buttons on the top part:
button_center = 0, 232.5
paused = False
gameOver = False
x2 = 0

def init():
    r, g, b = background_color
    glClearColor(r, g, b, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

def convert_coordinate(oldX, oldY): # ****
    newX = oldX - (Window_Width/2) + 6
    newY = (Window_Height/2 - oldY)*((500)/Window_Height) + 6
    return newX, newY

def draw_point(x, y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)
    glVertex2f(x, y)
    glEnd()


def draw_circle(x, y, c_x, c_y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)

    glVertex2f(x + c_x, y + c_y)
    glVertex2f(y + c_x, x + c_y)
    glVertex2f(y + c_x, -x + c_y)
    glVertex2f(x + c_x, -y + c_y)
    glVertex2f(-x + c_x, -y + c_y)
    glVertex2f(-y + c_x, -x + c_y)
    glVertex2f(-y + c_x, x + c_y)
    glVertex2f(-x + c_x, y + c_y)

    glEnd()

def draw_semi_circle(x, y, c_x, c_y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)

    glVertex2f(x + c_x, y + c_y)
    glVertex2f(y + c_x, x + c_y)
    glVertex2f(-y + c_x, x + c_y)
    glVertex2f(-x + c_x, y + c_y)
    glEnd()


def findZone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if(abs(dx) >= abs(dy)):
        if(dx > 0):
            if(dy > 0):
                zone = 0
            else:
                zone = 7
        else:
            if(dy > 0):
                zone = 3
            else:
                zone = 4
    else:
        if(dy > 0):
            if(dx > 0):
                zone = 1
            else:
                zone = 2
        else:
            if(dx > 0):
                zone = 6
            else:
                zone = 5

    return zone

def anyZoneToZoneZero(x0, y0, x1, y1, color):
    zone = findZone(x0, y0, x1, y1)
    if(zone == 0):
        drawLine_0(x0, y0, x1, y1, zone, color)
    if(zone == 1):
        drawLine_0(y0, x0, y1, x1, zone, color)
    if(zone == 2):
        drawLine_0(y0, -x0, y1, -x1, zone, color)
    if(zone == 3):
        drawLine_0(-x0, y0, -x1, y1, zone, color)
    if(zone == 4):
        drawLine_0(-x0, -y0, -x1, -y1, zone, color)
    if(zone == 5):
        drawLine_0(-y0, -x0, -y1, -x1, zone, color)
    if(zone == 6):
        drawLine_0(-y0, x0, -y1, x1, zone, color)
    if(zone == 7):
        drawLine_0(x0, -y0, x1, -y1, zone, color)


def zoneZeroToOriginalZone(x, y, zone):
    if(zone == 0):
        return (x, y)
    if(zone == 1):
        return (y, x)
    if(zone == 2):
        return (-y, x)
    if(zone == 3):
        return (-x, y)
    if(zone == 4):
        return (-x, -y)
    if(zone == 5):
        return (-y, -x)
    if(zone == 6):
        return (y, -x)
    if(zone == 7):
        return (x, -y)

def drawLine_8_waySymmetry(x0, y0, x1, y1, color):
    anyZoneToZoneZero(x0, y0, x1, y1, color)

def drawLine_0(x0, y0, x1, y1, zone, color):
    # MID-POINT LINE DRAWING ALGORITHM (FOR ZONE 0):
    dx = x1 - x0
    dy = y1 - y0
    delE = 2*dy
    delNE = 2*(dy-dx)
    d = 2*dy -dx
    x = x0
    y = y0

    while( x <= x1):
        originalX, originalY = zoneZeroToOriginalZone(x, y, zone)
        draw_point(originalX, originalY, pointSize, color)
        if(d < 0):
            d += delE
            x += 1
        else :
            d += delNE
            x += 1
            y += 1

def draw_enemyShip(color):
    x, y = enemyCenter
    drawLine_8_waySymmetry(x-15, y, x-15, y+12, color)
    drawLine_8_waySymmetry(x+15, y+12, x+15, y, color)
    drawLine_8_waySymmetry(x-15, y+12, x, y, color)
    drawLine_8_waySymmetry(x, y, x+15, y+12, color)
    drawLine_8_waySymmetry(x+15, y, x, y-12, color)
    drawLine_8_waySymmetry(x, y-12, x-15, y, color)


def draw_cross(color):
    x, y = button_center
    drawLine_8_waySymmetry(x+200, y-12.5, x+240, y+12.5, color)
    drawLine_8_waySymmetry(x+200, y+12.5, x+240, y-12.5, color)

def draw_backArrow(color):
    x, y = button_center
    draw_circle_midpoint(x-220, y, 18)
    drawLine_8_waySymmetry(x-238, y+5, x-250, y-10, color)
    drawLine_8_waySymmetry(x-238, y+5, x-225, y-10, color)

def draw_pause(color):
    x, y = button_center
    drawLine_8_waySymmetry(x-10, y+12.5, x-10, y-12.5, color)
    drawLine_8_waySymmetry(x+10, y+12.5, x+10, y-12.5, color)

def draw_play(color):
    x, y = button_center
    drawLine_8_waySymmetry(x-20, y+12.5, x+20, y, color)
    drawLine_8_waySymmetry(x+20, y, x-20, y-12.5, color)
    drawLine_8_waySymmetry(x-20, y-12.5, x-20, y+12.5, color)

def draw_pause_play(color):
    if(paused):
        draw_play(color)
    else:
        draw_pause(color)

def draw_userShip_triangle(color):
    x, y = userCurrentSpaceShipCenter
    drawLine_8_waySymmetry(x-80, y-50, x+80, y-50, color)

    drawLine_8_waySymmetry(x-65, y+20, x, y+60, color)
    drawLine_8_waySymmetry(x+65, y+20, x, y+60, color)

    drawLine_8_waySymmetry(x-65, y+10, x, y+50, color)
    drawLine_8_waySymmetry(x+65, y+10, x, y+50, color)

    drawLine_8_waySymmetry(x-15, y-50, x, y-60, color)
    drawLine_8_waySymmetry(x+15, y-50, x, y-60, color)
#20
def draw_left_misile(color):
    x, y = userCurrentSpaceShipCenter
    drawLine_8_waySymmetry(x-75, y-50, x-75, y+50, color)
    drawLine_8_waySymmetry(x-65, y-50, x-65, y+50, color)
    drawLine_8_waySymmetry(x-75, y+50, x-70, y+55, color)
    drawLine_8_waySymmetry(x-70, y+55, x-65, y+50, color)
    drawLine_8_waySymmetry(x-75, y-50, x-70, y-55, color)
    drawLine_8_waySymmetry(x-70, y-55, x-65, y-50, color)

def draw_right_misile(color):
    x, y = userCurrentSpaceShipCenter
    drawLine_8_waySymmetry(x+75, y-50, x+75, y+50, color)
    drawLine_8_waySymmetry(x+65, y-50, x+65, y+50, color)
    drawLine_8_waySymmetry(x+75, y+50, x+70, y+55, color)
    drawLine_8_waySymmetry(x+70, y+55, x+65, y+50, color)
    drawLine_8_waySymmetry(x+75, y-50, x+70, y-55, color)
    drawLine_8_waySymmetry(x+70, y-55, x+65, y-50, color)
def draw_right_bullet(color):
    x, y  = right_bullet_center
    if level == 1:
        drawLine_8_waySymmetry(x+70, y+55, x+70, y+60, color)
    elif level == 2:
        drawLine_8_waySymmetry(x+70, y+55, x+70, y+68, color)
    elif level == 3:
        drawLine_8_waySymmetry(x-70, y+55, x-70, y+68, color)
    elif level == 4:
        drawLine_8_waySymmetry(x-70, y+55, x-70, y+68, color)
    elif level == 5:
        drawLine_8_waySymmetry(x-70, y+55, x-70, y+68, color)
    elif level == 6:
        drawLine_8_waySymmetry(x-70, y+55, x-70, y+68, color)
    else:
        drawLine_8_waySymmetry(x+70, y+55, x+70, y+75, color)

def draw_left_bullet(color):
    x, y  = left_bullet_center
    if level == 1:
        drawLine_8_waySymmetry(x-70, y+55, x-70, y+60, color)
    elif level == 2:
        drawLine_8_waySymmetry(x-70, y+55, x-70, y+68, color)
    elif level == 3:
        drawLine_8_waySymmetry(x-70, y+55, x-70, y+68, color)
    elif level == 4:
        drawLine_8_waySymmetry(x-70, y+55, x-70, y+68, color)
    elif level == 5:
        drawLine_8_waySymmetry(x-70, y+55, x-70, y+68, color)
    elif level == 6:
        drawLine_8_waySymmetry(x-70, y+55, x-70, y+68, color)    
    else:
        drawLine_8_waySymmetry(x-70, y+55, x-70, y+75, color)

def draw_enemy_bullet(color):
    x, y = enemy_bullet_center
    drawLine_8_waySymmetry(x, y-15, x, y-20, color)

def draw_semi_circle_right(x, y, c_x, c_y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)

    glVertex2f(x + c_x, y + c_y) #1
    glVertex2f(y + c_x, x + c_y) #0
    glVertex2f(y + c_x, -x + c_y) #7
    glVertex2f(x + c_x, -y + c_y)  #6
    glEnd()

def draw_semi_circle_midpoint_right(c_x, c_y, r, color):
    x = 0
    y = r
    d = 5 - 4*r
    draw_semi_circle_right(x, y, c_x, c_y, circleSize, color)
    while(y > x):
        if(d < 0):
            d += 4*(2*x + 3)
        else:
            d += 4*(-2*y + 2*x +5)
            y-=1
        x+=1
        draw_semi_circle_right(x, y, c_x, c_y, circleSize, color)

def draw_semi_circle_for_5(x, y, c_x, c_y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)

    glVertex2f(x + c_x, y + c_y)
    glVertex2f(y + c_x, x + c_y)
    glVertex2f(y + c_x, -x + c_y)
    glVertex2f(x + c_x, -y + c_y)
    glVertex2f(-x + c_x, -y + c_y)
    glVertex2f(-x + c_x, y + c_y)
    glEnd()

def draw_semi_circle_midpoint_for_5(c_x, c_y, r, color):
    x = 0
    y = r
    d = 5 - 4*r
    draw_semi_circle_for_5(x, y, c_x, c_y, circleSize, color)
    while(y > x):
        if(d < 0):
            d += 4*(2*x + 3)
        else:
            d += 4*(-2*y + 2*x +5)
            y-=1
        x+=1
        draw_semi_circle_for_5(x, y, c_x, c_y, circleSize, color)

def draw_semi_circle_left(x, y, c_x, c_y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)
    glVertex2f(-x + c_x, -y + c_y)
    glVertex2f(-y + c_x, -x + c_y)
    glVertex2f(-y + c_x, x + c_y)
    glVertex2f(-x + c_x, y + c_y)
    glEnd()

def draw_semi_circle_midpoint_left(c_x, c_y, r, color):
    x = 0
    y = r
    d = 5 - 4*r
    draw_semi_circle_left(x, y, c_x, c_y, circleSize, color)
    while(y > x):
        if(d < 0):
            d += 4*(2*x + 3)
        else:
            d += 4*(-2*y + 2*x +5)
            y-=1
        x+=1
        draw_semi_circle_left(x, y, c_x, c_y, circleSize, color)
def draw_lvl():
    x,y = button_center
    drawLine_8_waySymmetry(x+70,240,x+70,220,(0.0,1.0,0.0))
    drawLine_8_waySymmetry(x + 78, 230, x + 85, 220, (0.0, 1.0, 0.0))
    drawLine_8_waySymmetry(x + 85, 220, x + 92, 230, (0.0, 1.0, 0.0))
    drawLine_8_waySymmetry(x+100,240,x+100,220,(0.0,1.0,0.0))


#Drawing scores
def draw_0(x, y, color):
    draw_circle_midpoint(x, y, 10)

def draw_1(x, y, color):
    drawLine_8_waySymmetry(x-10, y+5, x, y+10, color)
    drawLine_8_waySymmetry(x, y+10, x, y-10, color)

def draw_2(x, y, color):
    draw_semi_circle_midpoint(x, y+5, 5, color)
    drawLine_8_waySymmetry(x+6, y+6, x-5, y-10, color)
    drawLine_8_waySymmetry(x-5, y-10, x+10, y-10, color)

def draw_3(x, y, color):
    draw_semi_circle_midpoint_right(x, y+5, 5, color)
    draw_semi_circle_midpoint_right(x, y-5, 5, color)

def draw_4(x, y, color):
    drawLine_8_waySymmetry(x-10, y, x, y+10, color)
    drawLine_8_waySymmetry(x, y+10, x, y-10, color)
    drawLine_8_waySymmetry(x-10, y, x+5, y, color)

def draw_5(x, y, color):
    drawLine_8_waySymmetry(x-10, y+10, x+5, y+10, color)
    drawLine_8_waySymmetry(x-10, y+10, x-10, y, color)
    draw_semi_circle_midpoint_for_5(x-3, y-3, 7, color)

def draw_6(x, y, color):
    draw_semi_circle_midpoint_left(x, y, 10, color)
    draw_circle_midpoint(x-2, y-3.5, 6)

def draw_7(x, y, color):
    drawLine_8_waySymmetry(x-10, y+10, x, y+10, color)
    drawLine_8_waySymmetry(x, y+10, x-10, y-10, color)
#40
def draw_8(x, y, color):
    draw_circle_midpoint(x, y+5, 5)
    draw_circle_midpoint(x, y-5, 5)

def draw_9(x, y, color):
    draw_semi_circle_midpoint_right(x, y, 10, color)
    draw_circle_midpoint(x+2, y+3.5, 6)

def draw_score(actualScore, distance):
    x, y = button_center
    tempScore = actualScore
    remainder = tempScore%10
    while(tempScore != None):
        if(remainder == 0):
            draw_0(x-140 + distance, y, circleColor)   # what is distance?
        elif(remainder == 1):
            draw_1(x-140 + distance, y, circleColor)
        elif(remainder == 2):
            draw_2(x-140 + distance, y, circleColor)
        elif(remainder == 3):
            draw_3(x-140 + distance, y, circleColor)
        elif(remainder == 4):
            draw_4(x-140 + distance, y, circleColor)
        elif(remainder == 5):
            draw_5(x-140 + distance, y, circleColor)
        elif(remainder == 6):
            draw_6(x-140 + distance, y, circleColor)
        elif(remainder == 7):
            draw_7(x-140 + distance, y, circleColor)
        elif(remainder == 8):
            draw_8(x-140 + distance, y, circleColor)
        else:
            draw_9(x-140 + distance, y, circleColor)

        tempScore = tempScore // 10
        remainder = tempScore % 10
        distance -= 30     # why decrementing distance ?
        if(tempScore == 0):
            tempScore = None

def draw_score_partition(color, x, y):
    drawLine_8_waySymmetry(x, y+20, x, y-20, color)
    drawLine_8_waySymmetry(x-90, y+20, x+70, y+20, color)
    drawLine_8_waySymmetry(x-90, y-20, x+70, y-20, color)
    drawLine_8_waySymmetry(x-90, y+20, x-90, y-20, color)
    drawLine_8_waySymmetry(x+70, y+20, x+70, y-20, color)

def draw_circle_midpoint(c_x, c_y, r):
    x = 0
    y = r
    d = 5 - 4*r
    draw_circle(x, y, c_x, c_y, circleSize, circleColor)
    while(y > x):
        if(d < 0):
            d += 4*(2*x + 3)
        else:
            d += 4*(-2*y + 2*x +5)
            y-=1
        x+=1
        draw_circle(x, y, c_x, c_y, circleSize, circleColor)

def draw_semi_circle_midpoint(c_x, c_y, r, color):
    x = 0
    y = r
    d = 5 - 4*r
    draw_semi_circle(x, y, c_x, c_y, circleSize, color)
    while(y > x):
        if(d < 0):
            d += 4*(2*x + 3)
        else:
            d += 4*(-2*y + 2*x +5)
            y-=1
        x+=1
        draw_semi_circle(x, y, c_x, c_y, circleSize, color)



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    r, g, b = background_color
    glClearColor(r, g, b, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    draw_enemyShip(enemyColor)
    draw_cross(crossColor)
    draw_backArrow(backArrowColor)
    draw_pause_play(playPauseColor)
    draw_userShip_triangle(userCurrentSpaceShipColor)
    c_x, c_y = userCurrentSpaceShipCenter
    draw_circle_midpoint(c_x, c_y, 50)
    draw_left_misile(userCurrentSpaceShipColor)
    draw_right_misile(userCurrentSpaceShipColor)

    draw_right_bullet(userCurrentSpaceShipColor)
    draw_left_bullet(userCurrentSpaceShipColor)
    draw_enemy_bullet(userCurrentSpaceShipColor)
    draw_lvl()
    x,y = button_center
    if health_count == 13:
        draw_1(x+40,y,(1.0,0,0))
        draw_3(x+55,y,(1.0,0,0))
    elif health_count == 12:
        draw_1(x+40,y,(1.0,0,0))
        draw_2(x+55,y,(1.0,0,0))
    elif health_count == 11:
        draw_1(x+40,y,(1.0,0,0))
        draw_1(x+55,y,(1.0,0,0))
    elif health_count == 10:
        draw_1(x+40,y,(1.0,0,0))
        draw_0(x+55,y,(1.0,0,0))
    elif health_count == 9:
        draw_9(x+40,y,(1.0,0,0))
    elif health_count == 8:
        draw_8(x+40,y,(1.0,0,0))
    elif health_count == 7:
        draw_7(x+40,y,(1.0,0,0))
    elif health_count == 6:
        draw_6(x+40,y,(1.0,0,0))
    elif health_count == 5:
        draw_5(x+40,y,(1.0,0,0))
    elif health_count == 4:
        draw_4(x+40,y,(1.0,0,0))
    elif health_count == 3:
        draw_3(x+40,y,(1.0,0,0))
    elif health_count == 2:
        draw_2(x+40,y,(1.0,0,0))
    elif health_count == 1:
        draw_1(x,y,(1.0,0,0))
    else:
        draw_0(x+40,y,(1.0,0,0))

    if level == 0:
        draw_0(x+40,y,(1.0,0,0))
    elif level == 1:
        draw_1(x+125,y,(0.0,1.0,0))
    elif level == 2:
        draw_2(x+125,y,(0.0,1.0,0))
    elif level == 3:
        draw_3(x+125,y,(0.0,1.0,0))
    elif level == 4:
        draw_4(x+125,y,(0.0,1.0,0))
    elif level == 5:
        draw_5(x+125,y,(0.0,1.0,0))
    elif level == 6:
        draw_6(x+125,y,(0.0,1.0,0))    
    else:
        draw_7(x+125,y,(0.0,1.0,0))
    for star_coordinates in stars:
        x, y = star_coordinates
        draw_point(x, y, 1, (1.0, 1.0, 1.0))
    draw_score(score, 90)
    bx, by = button_center
    draw_score_partition(circleColor, bx - 100, by)
    draw_score(previous_score, 0)

    glutSwapBuffers()

def specialKeyListener(key, x, y):
    global userCurrentSpaceShipCenter
    x, y = userCurrentSpaceShipCenter
    if(not gameOver and not paused):
        if key==GLUT_KEY_LEFT and x>-250+80: x-=10
        if key==GLUT_KEY_RIGHT and x<250-80: x+=10
        if key==GLUT_KEY_UP and y<((Window_Height/2)-150): y+=10
        if key==GLUT_KEY_DOWN and y>(-(Window_Height/2)+200): y-=10
        userCurrentSpaceShipCenter = x, y
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global paused
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        btnX, btnY = button_center
        c_x, c_y = convert_coordinate(x, y)
        if(c_x < -150):  #
            c_x = c_x - 6
        if(c_x>=btnX+200 and c_x<=btnX+240 and c_y>=btnY-12.5 and c_y<=btnY+12.5):
            closeGame()
        elif(c_x>=btnX-240 and c_x<=btnX-200 and c_y>=btnY-12.5 and c_y<=btnY+12.5):
            reset()
        else:
            c_x, c_y = c_x - 6 , c_y  #
            if(not paused):
                if(c_x>=btnX-10 and c_x<=btnX+10 and c_y>=btnY-12.5 and c_y<=btnY+12.5):
                    paused = True
            else:
                if(c_x>=btnX-20 and c_x<=btnX+20 and c_y>=btnY-12.5 and c_y<=btnY+12.5):
                    paused = False

def closeGame():
    global previous_score
    print(f'Goodbye! Score: {score}')
    if sharp_shooter_badge and survivor_badge:
        print("You died as a Sharp Shooter and a Survivor!")
    elif sharp_shooter_badge:
        print("You died as a Sharp Shooter!")
    elif survivor_badge:
        print("You died as a Survivor!")
    if(score > previous_score):  # Saving Highest Score to file
        previous_score = score
    with open("score.txt", "w") as file:
        file.write(str(previous_score))
    glutLeaveMainLoop()

def reset():
    global start_time,speed, enemyCenter, score, gameOver, paused, userCurrentSpaceShipColor, enemyColor, health_count
    start_time = time.time()
    speed = 1
    health_count = 3
    score = 0
    paused = False
    gameOver = False
    enemyColor = random.choice(enemyColorList)
    x, y = enemyCenterInitalization
    enemyCenter = random.randrange(-230, 230), y
    userCurrentSpaceShipColor = 1.0, 1.0, 1.0
    print(f'Starting Over!')

def printGameState():
    global previous_score
    if(not gameOver):
        print(f'Score: {score}')
        if sharp_shooter_badge == False:
            print(f'{10 - sharp_shooter_count} more to get Sharp Shooter Badge!')
    else:
        print(f'Game Over!', end=" ")
        if sharp_shooter_badge and survivor_badge:
            print("You died as a Sharp Shooter and a Survivor!")
        elif sharp_shooter_badge:
            print("You died as a Sharp Shooter!")
        elif survivor_badge:
            print("You died as a Survivor!")
        if(score > previous_score):
            print(f'[You made new high score', end=" ")
            previous_score = score
        else:
            print(f'[Previous High Score : {previous_score}', end=" | ")
        print(f'Your Score : {score}]')
 #49
def idleFunction():
    if not gameOver and not paused:
       animate()

def animate():

    global survivor_badge, elapsed_time,sharp_shooter_badge, sharp_shooter_count, level_2_bonus, level_3_bonus, level_4_bonus, level_5_bonus, level_6_bonus, level_7_bonus, background_color, level, enemyCenter, speed, score, gameOver, enemyColor, userCurrentSpaceShipColor, left_bullet_center, right_bullet_center, health_count, userCurrentSpaceShipCenter, enemy_bullet_center, exhaust, enemyExhaust, stars
    elapsed_time = time.time() - start_time
    if elapsed_time >= 60 and  survivor_badge == False:
        survivor_badge = True
        print("Congrats Survivor! You successfully survived 2 minutes!")
    enemyX, enemyY = enemyCenter
    userCurrentSpaceShipX, userCurrentSpaceShipY = userCurrentSpaceShipCenter
    bulletX1, bulletY1 = left_bullet_center
    bulletX2, bulletY2 = right_bullet_center
    enemy_bullet_X, enemy_bullet_Y = enemy_bullet_center
    # ENEMY BULLET MOVEMENT
    if((enemy_bullet_X >= userCurrentSpaceShipX-75) and (enemy_bullet_X <= userCurrentSpaceShipX+75) and (enemy_bullet_Y-20 <= userCurrentSpaceShipY+55) and (enemy_bullet_Y-15 >= userCurrentSpaceShipY-55)):
        health_count-=1
        print("bullet hit")
        if(health_count==0):
            gameOver = True
            printGameState()
            userCurrentSpaceShipColor = 1.0, 0.0, 0.0
        if(health_count>0):
            userCurrentSpaceShipCenter = userSpaceShipInitialPosition
            enemy_bullet_center = enemyCenter

    elif(enemy_bullet_Y >= (-Window_Height/2)):   # If the enemy's bullet is within the window's height, its position is updated to move downward
        enemy_bullet_Y -= 3*(speed+(0.3*(level-1)))
        enemy_bullet_center = enemy_bullet_X, enemy_bullet_Y
    else:
        enemy_bullet_center = enemyCenter

    # USER SPACESHIP BULLET MOVEMENT
    if( bulletX1-70 >= enemyX-16 and bulletX1-70 <= enemyX+16 and bulletY1+60 >= enemyY-12 and bulletY1+55 <= enemyY+12):   # left bullet and spaceship collides
        left_bullet_center = userCurrentSpaceShipCenter
        enemyY = 200
        enemyX = random.randrange(-230, 230)
        enemyCenter = enemyX, enemyY
        score+=1
        sharp_shooter_count+=1
        if sharp_shooter_count>=10 and sharp_shooter_badge == False:
            sharp_shooter_badge = True
            print("Woah! You are a Sharp Shooter now!")
        printGameState()
    elif(bulletY1 < (Window_Height/2)-200): # left bullet didn't hit anything so keeps going up
        bulletY1+=10
        left_bullet_center = bulletX1, bulletY1
    else:
        left_bullet_center = userCurrentSpaceShipCenter

    if( bulletX2+70 >= enemyX-16 and bulletX2+70 <= enemyX+16 and bulletY2+60 >= enemyY-12 and bulletY2+55 <= enemyY+12):   # right bullet and spaceship collides
        right_bullet_center = userCurrentSpaceShipCenter
        enemyY = 200
        enemyX = random.randrange(-230, 230)
        enemyCenter = enemyX, enemyY
        score+=1
        sharp_shooter_count+=1
        if sharp_shooter_count>=10 and sharp_shooter_badge == False:
            sharp_shooter_badge = True
            print("Woah! You are a Sharp Shooter now!")
        printGameState()
    elif(bulletY2 < (Window_Height/2)-200):
        bulletY2+=10
        right_bullet_center = bulletX2, bulletY2
    else:
        right_bullet_center = userCurrentSpaceShipCenter

    if(enemyX+10 >= userCurrentSpaceShipX-75 and enemyX-13 <= userCurrentSpaceShipX+75 and enemyY-10 <= userCurrentSpaceShipY+55 and enemyY+10 >= userCurrentSpaceShipY-55):  # spaceship and enemyship collusion check
            health_count-=1
            if(health_count==0):
                gameOver = True
                printGameState()
                userCurrentSpaceShipColor = 1.0, 0.0, 0.0

            if(health_count>0):
                userCurrentSpaceShipCenter = userSpaceShipInitialPosition
            print("crash hit")
            enemyY = 200
            enemyX = random.randrange(-230, 230)
            enemyCenter = enemyX, enemyY
            enemyColor = random.choice(enemyColorList)
    elif(enemyY>(-240-30)):  # visible window r moddhe  ase kina. thakle sends it upward
        enemyY-=speed
        # enemyY-=0.0000001
        enemyCenter = enemyX, enemyY
    else:   # If the enemy spaceship moves out of the visible window, its position is reset to a new random position within the window
        enemyY = 200
        enemyX = random.randrange(-230, 230)
        enemyCenter = enemyX, enemyY
        enemyColor = random.choice(enemyColorList)
        sharp_shooter_count = 0
    speed+=0.0001
     # STARS
    for i in range(num_stars):
        x, y = stars[i]
        y -= (1)  # upward movement
        if(y < -Window_Height/2):
            y = Window_Height/2
        stars[i] = (x, y)
    if score> 18:
        level = 7
        if level_7_bonus:
            health_count+=3
            level_7_bonus = False
            print("Leveled Up!\nHealth increased")
    elif score > 15:
        level = 6
        if level_6_bonus:
            health_count+=2
            level_6_bonus = False
            print("Leveled Up!\nHealth increased")
    elif score> 12:
        level = 5
        if level_5_bonus:
            health_count+=2
            level_5_bonus = False
            print("Leveled Up!\nHealth increased")
    elif score > 9:
        level = 4
        if level_4_bonus:
            health_count+=1
            level_4_bonus = False
            print("Leveled Up!\nHealth increased")
    elif score> 6:
        level = 3
        if level_3_bonus:
            health_count+=1
            level_3_bonus = False
            print("Leveled Up!\nHealth increased")
    elif score > 3:
        level = 2
        if level_2_bonus:
            health_count+=1
            level_2_bonus = False
            print("Leveled Up!\nHealth increased")
    background_color = level_background_colors[level - 1]
    glutPostRedisplay()



def main():
    # Initialize stars
    for _ in range(num_stars):
        x = random.randint(-Window_Width//2, Window_Width//2)
        y = random.randint(-Window_Height//2, Window_Height//2)
        stars.append((x, y))

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(Window_Width, Window_Height)
    glutInitWindowPosition(560, 0)
    glutCreateWindow(b"Shooting StarShips")
    glutIdleFunc(idleFunction)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutDisplayFunc(display)
    init()
    glutMainLoop()
#54
if __name__ == "__main__":
    main()