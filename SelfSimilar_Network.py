import itertools
import numpy as np


def generator(num_digit,iterable):
    d = itertools.product(iterable, repeat=num_digit)
    result = []
    for i in d:
        result.append(list(i))
    return result

def link_number(num_digit, link_idset):
    ID_number =0
    for i in range(num_digit):
        power = (num_digit-1)-i
        ID_number = ID_number + (3**power)*link_idset[i]
    return ID_number

def conn_find(ID_set):
    if ID_set[-1] == 1:
        c = []
    elif ID_set[-1] == 0:
        c1 = list(ID_set)
        c2 = list(ID_set)
        c1[-1] = 1
        c2[-1] = 2
        c = [link_number(len(c1),c1),
              link_number(len(c2),c2)]
    i=-1
    reserve = list(ID_set)
    
    while ID_set[i]==2:
        i-=1
        if i == -1-len(ID_set):
            break
        else:
            pass
        if ID_set[i] !=0:
            c = []
        elif ID_set[i]==0:
            for k in range(i, 0, 1):
                if ID_set[k] == 2:
                    d1 = reserve
                    d1[k]=0
            c1 = list(d1)
            c2 = list(d1)
            c1[i] = 1   #TODO: some changes will be made here 
            c2[i] = 2
            c = [link_number(len(c1),c1),
                 link_number(len(c2),c2)]  
            
    return c

#H_order represents Horton order of each link
def Horton_order(conn_array):
    length = len(conn_array)
    H_order = np.zeros(length)  
    n = list(H_order).count(0)
    while n>0:
        for i in range(length):
            if conn_array[i] == []:
                H_order[i] = int(1)
            elif conn_array[i] !=[]:
                if H_order[conn_array[i][0]]!=0 and H_order[conn_array[i][1]]!=0:
                    if H_order[conn_array[i][0]] != H_order[conn_array[i][1]]:
                        s = max(H_order[conn_array[i][0]],H_order[conn_array[i][1]])
                        H_order[i] = s
                    else:
                        s = H_order[conn_array[i][0]] 
                        H_order[i] = s+1        
        n = list(H_order).count(0)
    return H_order

def SSN_create(order):
    l = [0,1,2]
    ID_set_ALL = generator(order, l)
    n_links = len(ID_set_ALL) ## the number of the links 
   
    network_info = {} # All information about the network is to be stored in 'network_info' 
    # CONNECTIVITY
    connectivity = [] # Connectivity of the network is to be stored in 'connectivity' list for convenience
    nextlink = np.zeros(n_links)-1 
    for i in range(n_links):
        network_info.update({link_number(order, ID_set_ALL[i]): 
            {'connectivity':conn_find(ID_set_ALL[i])}})
        connectivity.append(network_info[i]['connectivity'])  
    #DOWNSTREAM LINK
    # Indices of the nextlink array represent the link number, 
    # Each element in the array is the links to which the flow drains    
    nextlink = np.zeros(n_links)-1 
    for i in range(0, n_links):
        nextlink[connectivity[i][:]]=i
        nextlink = nextlink.astype(int) 
    #HORTON order
    horton_order = Horton_order(connectivity)
    for key in network_info:
        h = horton_order[key]
        network_info[key]['H_O'] = h
    
    return network_info 




link_ids = [0] 
junction_coord = [] # This list stores the coordinates of link junctions. (possible locations for dams)
pen_angle = [] #This list stores the pen angle at the links.

def generator_tree(turtle, branch_length, level, angle, print_id=False):

    global link_ids
    global junction_coord
    turtle.forward(branch_length/3)   #1/3
    if print_id:
        turtle.write(link_ids[-1], False, align = "center", font = ("Arial", 8, "bold") )
    link_ids.append((link_ids[-1]+1))
    m = turtle.position()
    a1 = turtle.heading()
       
    turtle.forward(branch_length*2/3)
    turtle.back(branch_length)    
    turtle.forward(branch_length)
    turtle.left(angle)
    turtle.forward(branch_length/3)
    if print_id:
        turtle.write(link_ids[-1], False, align = "center", font = ("Arial", 8, "normal") )
    link_ids.append(link_ids[-1]+1)
    f = turtle.position()
    a2 = turtle.heading()

    turtle.forward(branch_length*2/3)
    turtle.back(branch_length)
    turtle.right(2*angle)
    turtle.forward(branch_length/3)
    if print_id:
        turtle.write(link_ids[-1], False, align = "center", font = ("Arial", 8, "normal") )
    link_ids.append(link_ids[-1]+1)
    s = turtle.position()
    a3 = turtle.heading()

    turtle.forward(branch_length*2/3)
    junction_coord.extend([m,f,s])
    pen_angle.extend((a1, a2, a3))
    

def draw_recursive_tree(turtle, branch_length, level, angle, print_id=False):
    
    level = level - 1 # Correction of the order
    
    if level <2: 
        generator_tree(turtle, branch_length, level, angle, print_id)
        a = turtle.position()
        b = turtle.heading()
        turtle.right(angle)
        generator_tree(turtle, branch_length, level, angle, print_id)
        turtle.penup()
        turtle.setposition(a)
        turtle.pendown()
        turtle.setheading(b)
        turtle.left(2*angle)
        generator_tree(turtle, branch_length, level, angle, print_id)       
    else:  
        draw_recursive_tree(turtle, branch_length, level-1, angle, print_id)
        a = turtle.position()
        b = turtle.heading()
        if level%2 ==0:
            turtle.left(2*angle)
        else:
            turtle.right(angle)
        draw_recursive_tree(turtle, branch_length, level-1, angle, print_id)
        turtle.penup()
        turtle.setposition(a)
        turtle.pendown()
        turtle.setheading(b)
        if level%2 ==0:
            turtle.right(angle)
        else:
            turtle.left(2*angle)
        draw_recursive_tree(turtle, branch_length, level-1, angle, print_id)



def draw_dam(turtle, x, y, a, dam_size, color='red'):
    turtle.speed('fastest')
    turtle.penup()
    turtle.goto(x,y)
    turtle.setheading(a)
    turtle.color(color, color)
    turtle.pendown()
    turtle.begin_fill()
    turtle.right(90)
    turtle.forward(dam_size/2)
    turtle.right(90)
    turtle.forward(dam_size)
    turtle.right(90)
    turtle.forward(dam_size)
    turtle.right(90)
    turtle.forward(dam_size)
    turtle.right(90)
    turtle.forward(dam_size/2)
    turtle.end_fill()       
    turtle.penup()


def draw_controlpoint(turtle, x, y, a, shape_size, color='blue'):
    turtle.speed('fastest')
    turtle.penup()
    turtle.goto(x,y)
    turtle.setheading(a)
    turtle.color(color, color)
    turtle.pendown()
    turtle.begin_fill()
    turtle.right(90)
    turtle.forward(shape_size)
    turtle.left(90)
    turtle.forward(shape_size/2)
    turtle.left(90)
    turtle.forward(shape_size*2)
    turtle.left(90)
    turtle.forward(shape_size/2)
    turtle.left(90)
    turtle.forward(shape_size)
    turtle.end_fill() 


   

        