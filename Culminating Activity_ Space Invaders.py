#Set up the screen

import turtle
import os
import math
import random
import winsound
import sys
import time

#Uses the sys module and time
from time import sleep
for i in range(101):
    sys.stdout.write('\r')
    sys.stdout.write("[%-10s] %d%%" % ('='*i, 1*i))
    sys.stdout.flush()
    #It takes 3 milliseconds to load
    sleep(0.03)
    
###Set up the screen###
mainscreen = turtle.Screen()
#Screen Attributes#
mainscreen.bgcolor ("black")
mainscreen.title("Space Invaders")
#files/graphics must be on the same folder
mainscreen.bgpic("space_invaders_background.gif")

#Register the shapes
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")

###Draw border###
border_pen = turtle.Turtle()
#Border Attributes#
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
#Hides the turtle#
border_pen.hideturtle()

#SET THE SCORE to 0
score = 0

#Draw the score
score_pen = turtle.Turtle()
#Score's attributes
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()#not want to draw
score_pen.setposition(-290, 280)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font=("Arial", 13, "normal"))
score_pen.hideturtle()

###Create the player turtle###
player = turtle.Turtle()
#Turtle Attributes#
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

#Player moves 15 pixels each
playerspeed = 15

#Choose a number of enemies
number_of_enemies = 5
#Create an empty list of enemies
enemies = []

#Add enemies to the list
for i in range(number_of_enemies):
#Create the enemy/invader using a turtle
    enemies.append(turtle.Turtle())
#Enemy attributes
for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)

    #x-coordinate(x)
    x = random.randint(-200, 200)
    #y-coordinate(y)
    y = random.randint(100, 250)
    #(x,y) coordinates
    enemy.setposition(x, y)

#enemy is slower than player
enemyspeed = 2

#Create the player's bullet
bullet = turtle.Turtle()
#Bullet Attributes
bullet.color ("yellow")
bullet.shape ("circle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.6,0.6)
bullet.hideturtle()

bulletspeed = 20

#Define bullet state
#Ready - ready to fire
#fire - bullet is firing
bulletstate = "ready"

#Move the player left and right
#for left
def move_left():
    #X-coordinate
    #Game starts with 0
    x = player.xcor()
    #Takes the current value of x, subtracts player speed and assign that to X
    x -= playerspeed
    ##BOUNDARY CHECKING##
    #Blocks the player from moving below -280
    if x < -280:
        x = -280
    player.setx(x)

#for right
def move_right():
    #set x
    x = player.xcor()
    #Takes the current value of x, subtracts player speed and assign that to X
    x += playerspeed
    ##BOUNDARY CHECKING##
    #Blocks the player from moving more than 280
    if x > 280:
        x = 280
    player.setx(x)

#firing the bullet
def fire_bullet():
    #Declare bulletstate as if it needs to be changed
    global bulletstate
    if bulletstate == "ready":
        #This is for the laser sound#laser sounds plays when the bullet is in ready state
        winsound.PlaySound("laser.wav", winsound.SND_ASYNC)
        bulletstate = "fire"
        #Move the bullet to above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

#defining the collision
def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance <15:
        return True
    else:
        return False

#Create keyboard bindings
turtle.listen()#follow the keyboard bindins
turtle.onkey(move_left, "Left")#left arrow
turtle.onkey(move_right, "Right")#right arrow
turtle.onkey(fire_bullet, "space")#space to fire bullet

#Main Game Loop
while True:

    for enemy in enemies:
        #Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        #Move the enemy back and down
        #Right side
        if enemy.xcor() > 280:
            #Move all enemies down
            for e in enemies:
                #y coordinate
                y = e.ycor()
            s    y -= 40
                e.sety(y)
            #Change enemy direction
            enemyspeed *= -1
            
        #Left side
        if enemy.xcor() < -280:
            #Move all enemies down
            for e in enemies:
                #y coordinate
                y = e.ycor()
                y -= 40
                e.sety(y)
            #Change enemy direction
            enemyspeed *= -1
            
        #Check for a collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            #This is for the explosion sound
            winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
            #Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition (0, -400)

            #Reset the enemy
            #x-coordinate(x)
            x = random.randint(-200, 200)
            #y-coordinate(y)
            y = random.randint(100, 250)
            #(x,y) coordinates
            enemy.setposition(x, y)

            #Update the score
            score += 10
            scorestring = "Score: %s" %score
            #clears the score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 13, "normal"))

        #Check for a collision between the player and the enemy
        if isCollision(player, enemy):
            #This is for the explosion sound
            winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
            player.hideturtle()
            enemy.hideturtle()

            #Draw the Game over
            gameover_pen = turtle.Turtle()
            #Game Over's attributes
            gameover_pen.speed(0)
            gameover_pen.color("white")
            gameover_pen.penup()#not want to draw
            gameover_pen.setposition(10, 0)
            gameoverstring = "Game Over!" 
            gameover_pen.write(gameoverstring, False, align="center",font=("Arial", 60, "bold"))
            gameover_pen.hideturtle()
            
            gameoverstring = "Game Over!" 
            print ("Game Over")
            break
        
    #Move the bullet
    #state controls the bullet condition
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    #Check to see if the bullet is going to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"
        
delay = raw_input("Press enter to finish")
