from SelfSimilar_Network import *
import turtle 




WIDTH = 1  ##TODO: This has not been used yet. The width of the lines will be set according to their Horton order
ANGLE = 40
BRANCH_LENGTH = 100
CONTROLPOINT_SIZE = 25
DAM_SIZE = 25  
ORDER = 3

INITIAL_PEN_POSITION = (0.0, -300)


if __name__ == "__main__":
    
    network_info = SSN_create(ORDER)
    screen = turtle.Screen()  
    screen.setup(width=900,height=1000)
    screen.title(f"Order {ORDER} Deterministic Mandelbrot-Vicsek Tree")


    pen = turtle.Turtle()
    pen.penup()
    pen.setposition(INITIAL_PEN_POSITION)
    pen.pendown()
    pen.showturtle()
    pen.speed('fastest')
    pen.left(90)   
    draw_recursive_tree(pen, BRANCH_LENGTH, ORDER, ANGLE, print_id=True)

    dam_id = [3, 9, 15, 20]
    for id in dam_id:
        draw_dam(pen, junction_coord[id][0], junction_coord[id][1], pen_angle[id], DAM_SIZE, color='#009988')

    control_point = [0]
    for id in control_point:
        draw_controlpoint(pen,  junction_coord[id][0], junction_coord[id][1], pen_angle[id], CONTROLPOINT_SIZE, color='#9970AB')
    pen.hideturtle()
    turtle.getscreen().getcanvas().postscript(file=f'SSN_{ORDER}.ps')
    screen.exitonclick()
