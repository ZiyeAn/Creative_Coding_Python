from turtle import *
import math

def draw_leaves(x,y):
    left(60)
    for i in range(5):
        left(2)
        forward()

def draw_flower(x, y):
    penup()
    goto(x, -200)
    pendown()
    goto(x, y)
    for i in range(5):
        circle(20)
        left(360/5)
onscreenclick(draw_flower)
mainloop()
