import tkinter as tk
from random import randrange
from PIL import Image, ImageTk
import os
from cars import cars

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
        self.footpath1 = tk.Canvas(self.w, height = 50, width = 700, highlightbackground = 'black')
        self.footpath1.grid(row = 0, column = 0, rowspan = 1, columnspan = 1)
        self.color_footpath(self.footpath1, 7)
        self.road = tk.Canvas(self.w, height = 300, width = 700, bg = 'light blue', highlightbackground = 'black')
        # self.road.focus_set()
        self.road.grid(row = 1, column = 0, rowspan = 1, columnspan = 1)
        self.footpath2 = tk.Canvas(self.w, height = 50, width = 700, highlightbackground = 'black')
        self.footpath2.grid(row = 7, column = 0, rowspan = 1, columnspan = 1)
        self.color_footpath(self.footpath2, 7)
        x = 50
        l = []
        for i in range(5):
            l.append(self.road.create_line(0, x, 700, x))
            x += 50
        for j in self.car_coords.car_dict:
            f = randrange(3)
            if self.car_coords.car_dict[j][0] == 'r':
                p = os.path.join(self.root, 'right_cars', self.right_img_files[f])
                self.car_imgs[j] = ['r', self.draw_car(p, *self.car_coords.car_dict[j][1:3])]
            else:
                p = os.path.join(self.root, 'left_cars', self.left_img_files[f])
                self.car_imgs[j] = ['l', self.draw_car(p, *self.car_coords.car_dict[j][1:3])]
        self.pl = player_GUI(self.footpath2, 335, 0)
        self.w.bind('<Left>', lambda q: self.left_key())
        self.w.bind('<Right>', lambda q: self.right_key())
        self.w.bind('<Up>', lambda q: self.up_key())
        self.w.bind('<Down>', lambda q: self.down_key())
        self.run()
    def left_key(self):
        self.pl.c.move(self.pl.obj, -30, 0)
    def right_key(self):
        self.pl.c.move(self.pl.obj, 30, 0)
    def up_key(self):
        x1, y1, x2, y2 = self.pl.c.coords(self.pl.obj)
        if self.pl.c == self.footpath2:
            self.pl.c.delete(self.pl.obj)
            self.pl.c = self.road
            self.pl.obj = self.pl.c.create_rectangle(x1, 250, x2, 300, fill = 'red', outline = 'black')
        elif self.pl.c == self.road and y1 == 0:
            self.pl.c.delete(self.pl.obj)
            self.pl.c = self.footpath1
            self.pl.obj = self.pl.c.create_rectangle(x1, 0, x2, 50, fill = 'red', outline = 'black')
            self.won = 1
            self.cancel = True
        else:
            self.pl.c.move(self.pl.obj, 0, -50)
    def down_key(self):
        x1, y1, x2, y2 = self.pl.c.coords(self.pl.obj)
        if self.pl.c == self.footpath2:
            pass
        elif self.pl.c == self.road and y2 == 300:
            self.pl.c.delete(self.pl.obj)
            self.pl.c = self.footpath2
            self.pl.obj = self.pl.c.create_rectangle(x1, 0, x2, 50, fill = 'red', outline = 'black')
        else:
            self.pl.c.move(self.pl.obj, 0, 50)
    def color_footpath(self, c, n):
        h = int(c['height'])
        w = int(c['width'])
        for i in range(n):
            if i%2:
                c.create_rectangle(i*(w/n), 0, i*(w/n)+(w/n), h, fill = 'yellow')
            else:
                c.create_rectangle(i*(w/n), 0, i*(w/n)+(w/n), h, fill = 'black')
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
                    self.car_coords.l_update(key, reset = 1)
                    if self.road.coords(self.car_imgs[key][1].obj)[0] == -50:
                        self.road.move(self.car_imgs[key][1].obj, 800, 0)
                        self.car_coords.l_update(key, reset = 1)
            # self.road.update()
            self.after_id = self.road.after(50, lambda: self.run())
        else:
            self.w.after_cancel(self.after_id)
            if self.won:
                self.GO = self.road.create_text(350, 150, text = 'YOU WON!!!', font=('Helvetica 25 bold'))
            else:
                self.GO = self.road.create_text(350, 150, text = 'GAME OVER\nYOU LOSE!!!', font=('Helvetica 25 bold'))

class car_GUI:
    def __init__(self, c, img, x, y):
        self.img = (Image.open(img)).resize((100, 50), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.img)
        # c.photo = photo
        self.obj = c.create_image(x, y, image = self.photo)
class player_GUI:
    def __init__(self, c, x, y):
        self.c = c
        self.obj = c.create_rectangle(x, y, x+30, y+50, fill = 'red', outline = 'black')

app = environ()
tk.mainloop()
