angles = [0, PI / 3, - PI / 3 ]
new_ind = 2

def setup():
    size(400, 400)
    background(0)
    stroke_weight(2)
    fill(113, 147, 130)
    stroke(0)

def draw():
    background(0)
    for angle in angles:
        v_shape(200, 200, angle)

def mouse_pressed():
    global new_ind
    new_angle = angles[new_ind] - PI / 3
    angles.append(new_angle)
    new_ind += 1

def v_shape(x_pos, y_pos, angle):
    push()
    translate(x_pos, y_pos)
    rotate(angle)
    
    for i in range(1, 90, 10):
        triangle(0, 0 + 1.73 * i, -100 + i, 173, 100 - i, 173)
    
    fill(0)
    triangle(0, 1.73 * 80, -20, 173, 20, 173)
    pop()
