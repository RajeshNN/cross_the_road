import tkinter as tk
from random import randrange
from PIL import Image, ImageOps, ImageTk
import os
from cars import cars
from player import player

class environ:
    def __init__(self):
        self.w = tk.Tk(className = ' Cross The Road')
        self.car_imgs = {}
        self.cancel = False
        self.won = 0
        self.root = os.getcwd()
        self.right_img_files = ['redright.png', 'blueright.png', 'greenright.png']
        self.left_img_files = ['redleft.png', 'blueleft.png', 'greenleft.png']
        self.car_coords = cars()
        self.player = player()
        self.footpath1 = tk.Canvas(self.w, height = 50, width = 700, highlightbackground = 'black')
        self.footpath1.grid(row = 0, column = 0, rowspan = 1, columnspan = 1)
        self.color_footpath(self.footpath1, 7)
        self.road = tk.Canvas(self.w, height = 300, width = 700, bg = 'light blue', highlightbackground = 'black')
        self.road.grid(row = 1, column = 0, rowspan = 1, columnspan = 1)
        self.footpath2 = tk.Canvas(self.w, height = 50, width = 700, highlightbackground = 'black')
        self.footpath2.grid(row = 7, column = 0, rowspan = 1, columnspan = 1)
        self.color_footpath(self.footpath2, 7)
        x = 50
        l = []
        for i in range(5):
            l.append(self.road.create_line(0, x, 700, x, width = 3))
            x += 50
        for j in self.car_coords.car_dict:
            f = randrange(3)
            if self.car_coords.car_dict[j][0] == 'r':
                p = os.path.join(self.root, 'right_cars', self.right_img_files[f])
                self.car_imgs[j] = ['r', self.draw_car(p, *self.car_coords.car_dict[j][1:3])]
            else:
                p = os.path.join(self.root, 'left_cars', self.left_img_files[f])
                self.car_imgs[j] = ['l', self.draw_car(p, *self.car_coords.car_dict[j][1:3])]
        self.pl = player_GUI(self.footpath2, self.player.posit[1], 25, os.path.join(self.root, 'chicken.png'))
        self.w.bind('<Left>', lambda q: self.left_key())
        self.w.bind('<Right>', lambda q: self.right_key())
        self.w.bind('<Up>', lambda q: self.up_key())
        self.w.bind('<Down>', lambda q: self.down_key())
        self.run()
    def left_key(self):
        x1, y1 = self.pl.c.coords(self.pl.obj)
        self.pl.c.delete(self.pl.obj)
        self.pl.obj = self.pl.c.create_image(x1-30, y1, image = self.pl.mphoto)
        self.pl.r = 0
        self.player.update_xpos(x1-30)
    def right_key(self):
        x1, y1 = self.pl.c.coords(self.pl.obj)
        self.pl.c.delete(self.pl.obj)
        self.pl.obj = self.pl.c.create_image(x1+30, y1, image = self.pl.photo)
        self.pl.r = 1
        self.player.update_xpos(x1+30)
    def up_key(self):
        x1, y1 = self.pl.c.coords(self.pl.obj)
        if self.pl.c == self.footpath2:
            self.pl.c.delete(self.pl.obj)
            self.pl.c = self.road
            if self.pl.r:
                self.pl.obj = self.pl.c.create_image(x1, 275, image = self.pl.photo)
            else:
                self.pl.obj = self.pl.c.create_image(x1, 275, image = self.pl.mphoto)
            self.player.update_lane(6)
        elif self.pl.c == self.road and y1 == 25:
            self.pl.c.delete(self.pl.obj)
            self.pl.c = self.footpath1
            if self.pl.r:
                self.pl.obj = self.pl.c.create_image(x1, 25, image = self.pl.photo)
            else:
                self.pl.obj = self.pl.c.create_image(x1, 25, image = self.pl.mphoto)
            self.won = 1
            self.cancel = True
        else:
            self.pl.c.move(self.pl.obj, 0, -50)
            self.player.update_lane(int(y1/50))
    def down_key(self):
        x1, y1  = self.pl.c.coords(self.pl.obj)
        if self.pl.c == self.footpath2:
            pass
        elif (self.pl.c == self.road) and (y1 == 275.0):
            self.pl.c.delete(self.pl.obj)
            self.pl.c = self.footpath2
            self.player.update_lane(int(0))
            if self.pl.r:
                self.pl.obj = self.pl.c.create_image(x1, 25, image = self.pl.photo)
            else:
                self.pl.obj = self.pl.c.create_image(x1, 25, image = self.pl.mphoto)
        else:
            self.pl.c.move(self.pl.obj, 0, 50)
            self.player.update_lane(int(y1/50) + 1)
    def freeze(self):
        pass
    def call_to_freeze(self):
        self.w.bind('<Left>', lambda q: self.freeze())
        self.w.bind('<Right>', lambda q: self.freeze())
        self.w.bind('<Up>', lambda q: self.freeze())
        self.w.bind('<Down>', lambda q: self.freeze())
    def color_footpath(self, c, n):
        h = int(c['height'])
        w = int(c['width'])
        for i in range(n):
            if i%2:
                c.create_rectangle(i*(w/n), 0, i*(w/n)+(w/n), h, fill = 'yellow')
            else:
                c.create_rectangle(i*(w/n), 0, i*(w/n)+(w/n), h, fill = 'black')
    def check_collision(self, lane, xpos):
        if lane:
            for car in self.car_coords.lane_dict[lane]:
                llim = self.car_coords.car_dict[car][1] - 50
                rlim = self.car_coords.car_dict[car][1] + 50
                if xpos+15>llim and xpos-15<rlim:
                    self.cancel = True
    def draw_car(self, img, a, b):
        return car_GUI(self.road, img, a, b)
    def run(self):
        if not self.cancel:
            for key in self.car_imgs:
                if self.car_imgs[key][0] == 'r':
                    self.road.move(self.car_imgs[key][1].obj, 5, 0)
                    self.car_coords.r_update(key)
                    if self.road.coords(self.car_imgs[key][1].obj)[0] == 750:
                        self.road.move(self.car_imgs[key][1].obj, -800, 0)
                        self.car_coords.r_update(key, reset = 1)
                else:
                    self.road.move(self.car_imgs[key][1].obj, -5, 0)
                    self.car_coords.l_update(key)
                    if self.road.coords(self.car_imgs[key][1].obj)[0] == -50:
                        self.road.move(self.car_imgs[key][1].obj, 800, 0)
                        self.car_coords.l_update(key, reset = 1)
            self.check_collision(*self.player.posit)
            self.after_id = self.road.after(50, lambda: self.run())
        else:
            self.w.after_cancel(self.after_id)
            self.call_to_freeze()
            if self.won:
                self.wO = self.road.create_text(350, 150, text = 'YOU WON!!!', font=('Helvetica 30 bold'), fill = 'white')
                self.BO = self.road.create_text(354, 154, text = 'YOU WON!!!', font=('Helvetica 30 bold'), fill = 'black')
                self.RO = self.road.create_text(352, 152, text = 'YOU WON!!!', font=('Helvetica 30 bold'), fill = 'red')
            else:
                self.WO = self.road.create_text(350, 150, text = 'GAME OVER\nYOU LOSE!!!', font=('Helvetica 30 bold'), fill = 'white')
                self.BO = self.road.create_text(354, 154, text = 'GAME OVER\nYOU LOSE!!!', font=('Helvetica 30 bold'), fill = 'black')
                self.RO = self.road.create_text(352, 152, text = 'GAME OVER\nYOU LOSE!!!', font=('Helvetica 30 bold'), fill = 'red')

class car_GUI:
    def __init__(self, c, img, x, y):
        self.img = (Image.open(img)).resize((100, 50), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.img)
        self.obj = c.create_image(x, y, image = self.photo)
class player_GUI:
    def __init__(self, c, x, y, img):
        self.c = c
        self.r = 1
        self.img = Image.open(img).resize((30, 50), Image.ANTIALIAS)
        self.mimg = ImageOps.mirror(self.img)
        self.photo = ImageTk.PhotoImage(self.img)
        self.mphoto = ImageTk.PhotoImage(self.mimg)
        self.obj = c.create_image(x, y, image = self.photo)

app = environ()
tk.mainloop()
