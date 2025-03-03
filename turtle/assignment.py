import turtle
import random

def draw_square_pattern(t, x, y, size, step, depth):
    t.penup()
    t.goto(x, y)
    t.pendown()
    
    for i in range(depth):
        t.forward(size - step * i)
        t.right(90)
        t.forward(size - step * i)
        t.right(90)
        t.forward(size - step * (i + 1))
        t.right(90)
        t.forward(size - step * (i + 1))
        t.right(90)


screen = turtle.Screen()
screen.bgcolor("white")
t = turtle.Turtle()
t.speed(0)
t.pensize(5)

def random_color():
    return (random.random(), random.random(), random.random())


size = 300 
step = 20 
depth = 30
start_x, start_y = -size, size  
positions = [(start_x, start_y)]  


def on_click(x, y):
    t.pencolor(random_color())  
    last_x, last_y = positions[-1] 
    draw_square_pattern(t, last_x, last_y, size, step, depth)  


t.pencolor(random_color())
draw_square_pattern(t, start_x, start_y, size, step, depth)

screen.onclick(on_click)
screen.mainloop()