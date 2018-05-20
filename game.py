from tkinter import Tk, Canvas, mainloop, NW, N, Label, NE, LEFT, E, W, StringVar
from PIL import Image, ImageTk
import time
import random


hp = 3


window_width = 450
window_height = 800
tk = Tk()
c = Canvas(tk, width=window_width, height=window_height, bg='white')
c.pack()
sky_image = ImageTk.PhotoImage(Image.open('assests/sky.jpg').resize((window_width, window_height)))
ship_image = ImageTk.PhotoImage(Image.open('assests/ship.gif').resize((60, 60)))
sky = c.create_image(0, 0, image=sky_image, anchor=NW)
ship = c.create_image(195, 600, image=ship_image, anchor=NW)
bullet_image = ImageTk.PhotoImage(Image.open('assests/laser.gif').resize((5, 30)))
meteor_image = ImageTk.PhotoImage(Image.open('assests/meteor.gif').resize((40, 80)))
bullets = []
meteors = []



def label():
    global HPLabel
    HPLabel = c.create_text(10, 10, width = 300, text="Health Points: "+ str(hp), fill = '#fff', anchor = NW)

def get_bullet(x, y):
    bullet = c.create_image(x+3, y+18, image=bullet_image, anchor= E)
    bullets.append(bullet)


def knopki(key):
    x, y = c.coords(ship)
    if key.char == 'a':
        if x > 0:
            c.move(ship, - 10, 0)
    if key.char == 'd':
        if x < 390:
            c.move(ship, 10, 0)
    if key.char == 'w':
        if y > 0:
            c.move(ship, 0, -10)
    if key.char == 's':
        if y < 720:
            c.move(ship, 0, 10)
    if key.char == ' ':
        x, y = c.coords(ship)
        get_bullet(x+30, y-20)


def loop():
    for bullet in bullets:
        c.move(bullet, 0, -10)
    c.after(5, loop)



def add_meteor():
    global hp
    vremya = random.randint(750, 1500)
    distance = random.randint(0, 410)
    meteor = c.create_image(distance, -80, image=meteor_image, anchor=NW)
    meteors.append(meteor)

    c.after(vremya, add_meteor)


def kollusion():
    global hp
    for meteor in meteors[:]:
        meteorx, meteory = c.coords(meteor)
        shipx, shipy = c.coords(ship)
        if (meteory + 80 > shipy) and (meteory < shipy + 60) and (meteorx + 40 > shipx) and (meteorx < shipx + 60):
            c.delete(meteor)
            meteors.remove(meteor)
            hp -= 1
            GameOver()
            c.delete(HPLabel)
            label()
    for meteor in meteors[:]:
        meteorx, meteory = c.coords(meteor)
        if meteory > 750:
            c.delete(meteor)
            meteors.remove(meteor)
    c.after(50, kollusion)

def dvizh():
    for meteor in meteors:
        c.move(meteor, 0, 3)
    c.after(50, dvizh)

def GameOver():
    global hp
    global window_height
    global window_width
    if hp == 0:
        c.delete(ship)
        EndText = c.create_text(100, 300, width=500, text="Game over", fill='#FF0000', anchor=NW, font = ("Courier",44))
        c.after(3000, lambda: exit())

def ShootingMeteors():
    for i, bullet in enumerate(bullets):
        for j, meteor in enumerate(meteors):
            bulletx, bullety = c.coords(bullet)
            meteorx, meteory = c.coords(meteor)
            if (meteorx < bulletx < meteorx + 40) and (meteory< bullety< meteory + 80):
                c.delete(bullet)
                c.delete(meteor)
                meteors.pop(j)
                bullets.pop(i)
                break
    c.after(50, ShootingMeteors)

def SummonStarter(key):
    if key.char == ' ':
        starter()




tk.bind("<KeyPress>", knopki)
add_meteor()
dvizh()
loop()
kollusion()
label()
ShootingMeteors()
mainloop()
