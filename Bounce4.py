#Bounce4 (add Vector Bounds)
#Josh Bowen
#5/3/2022

import turtle
import random
import math

class Ball():

    def __init__(self, name, color, surfaces, number_of_surfaces, ht):
        
        self.surfaces = surfaces
        self.number_of_surfaces = number_of_surfaces
        
        theta = 155#random.randrange(0,360)*math.pi/100
        self.op = [0,0]
        self.v = [math.cos(theta), math.sin(theta)]
        self.t = 0
        self.intercept = [0,0]

        self.name = name
        self.name = turtle.Turtle()
        self.name.ht()
        self.name.up()
        self.name.goto(self.op[0],self.op[1])
        self.name.down()
        if ht:
            self.name.ht()
        else:
            self.name.st()
        self.name.color(color)
        self.name.speed(4)
        self.name.shape("circle")

    def travel(self):
        
        possible_t = []
        t = 0
        
        for i in range(self.number_of_surfaces):
            op_other = [self.surfaces[i][0],self.surfaces[i][1]]
            v_other = [self.surfaces[i][2] - self.surfaces[i][0], self.surfaces[i][3] - self.surfaces[i][1]]

            if v_other[1] == 0:
                t = (op_other[1] - self.op[1])/(self.v[1])
                if t > 0:
                    possible_t.append(t)
            elif v_other[0] == 0:
                t = (op_other[0] - self.op[0])/(self.v[0])
                if t > 0:
                    possible_t.append(t)
            else:
                #solved system of 2 equations with s and t for vector parameterizations
                t = (op_other[0] - self.op[0] + (self.op[1]*v_other[0]/v_other[1]) - (op_other[1]*v_other[0]/v_other[1])) / (self.v[0] - (v_other[0]*self.v[1]/v_other[1]))
                if t > 0:
                    possible_t.append(t)


        for i in range(len(possible_t)):
            if possible_t[i] < 1:
                possible_t[i] += 9999999999
        self.t = min(possible_t)
        self.intercept = [int(round(self.op[0] + self.v[0]*self.t,0)), int(round(self.op[1] + self.v[1]*self.t,0))]
        self.name.goto(self.intercept)
            
    def bounce(self):
        #find surface
        surface_index = 99
        corner = False
        v_ = []
        unit_normal = []
        x = 0
        y = 0
        
        for i in range(self.number_of_surfaces):
            
            if self.surfaces[i][0] > self.surfaces[i][2]:
                large_x = self.surfaces[i][0]
                small_x = self.surfaces[i][2]
            else:
                large_x = self.surfaces[i][2]
                small_x = self.surfaces[i][0]

            if self.surfaces[i][1] > self.surfaces[i][3]:
                large_y = self.surfaces[i][1]
                small_y = self.surfaces[i][3]
            else:
                large_y = self.surfaces[i][3]
                small_y = self.surfaces[i][1]
                
            if self.intercept[0] >= small_x and self.intercept[0] <= large_x and self.intercept[1] >= small_y and self.intercept[1] <= large_y:
                surface_index = i
                
            if (self.intercept[0] == small_x or self.intercept[0] == large_x) and (self.intercept[1] == small_y or self.intercept[1] == large_y):
                corner = True

        v_ = [self.surfaces[surface_index][2] - self.surfaces[surface_index][0], self.surfaces[surface_index][3] - self.surfaces[surface_index][1]]
        unit_normal = [(-1*v_[1])/math.sqrt(v_[0]**2 + v_[1]**2), (v_[0])/math.sqrt(v_[0]**2 + v_[1]**2)]       

        #Concept from stackoverflow.com
        x = self.v[0] - 2*(self.v[0]*unit_normal[0] + self.v[1]*unit_normal[1])*unit_normal[0]
        y = self.v[1] - 2*(self.v[1]*unit_normal[1] + self.v[0]*unit_normal[0])*unit_normal[1]


        if corner:
            x = -1*self.v[0]
            y = -1*self.v[1]
            
        self.v = [x,y]
        self.op = self.intercept
        

def bounds():
    wn = turtle.Screen()
    wn.bgcolor("black")
    output = []
    
    wn.onscreenclick(output.append([x,y]))
    return output
            
def main():
    surfaces = [(-150,-150,150,-150),(150,-150,150,150),(150,150,-200,200),(-200,200,-150,-150)]
    number_of_surfaces = 4

    wn = turtle.Screen()
    wn.bgcolor("Black")

    bound = turtle.Turtle()
    bound.color("White")
    bound.speed(0)
    bound.width(5)
    bound.ht()
        
    for i in range(len(surfaces)):
        bound.up()
        bound.goto(surfaces[i][0], surfaces[i][1])
        bound.down()
        bound.goto(surfaces[i][2], surfaces[i][3])

    my_ball = Ball("tennis", "lightblue", surfaces, number_of_surfaces, False)
    cool_effect = Ball("tennis", "black", surfaces, number_of_surfaces, True)
    
    while True:
        my_ball.travel()
        my_ball.bounce()
        #cool_effect.travel()
        #cool_effect.bounce()
main()

#NOTE: this version does not work for shapes inside shapes! Fix that in next version
