import tkinter as tk
from random import randrange
from PIL import Image, ImageTk
import os
from cars import cars

class environ:
    def __init__(self, car_coords):
        self.w = tk.Tk(className = 'New Game')
        self.cars = {}
        self.cancel = False
        self.root = os.getcwd()
        self.right_img_files = ['redright.png', 'blueright.png', 'greenright.png']
        self.left_img_files = ['redleft.png', 'blueleft.png', 'greenleft.png']
        self.car_coords = car_coords
        self.footpath1 = tk.Canvas(self.w, height = 50, width = 700, highlightbackground = 'black')
        self.footpath1.grid(row = 0, column = 0, rowspan = 1, columnspan = 1)
        self.color_footpath(self.footpath1, 7)
        self.road = tk.Canvas(self.w, height = 300, width = 700, bg = 'light blue', highlightbackground = 'black')
        self.road.focus_set()
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
                self.cars[j] = ['r', self.draw_car(p, *self.car_coords.car_dict[j][1:3])]
            else:
                p = os.path.join(self.root, 'left_cars', self.left_img_files[f])
                self.cars[j] = ['l', self.draw_car(p, *self.car_coords.car_dict[j][1:3])]
        self.run()

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
            for key in self.cars:
                if self.cars[key][0] == 'r':
                    self.road.move(self.cars[key][1].obj, 5, 0)
                    self.car_coords.r_update(key)
                    if self.road.coords(self.cars[key][1].obj)[0] == 750:
                        self.road.move(self.cars[key][1].obj, -800, 0)
                        self.car_coords.r_update(key, reset = 1)
                else:
                    self.road.move(self.cars[key][1].obj, -5, 0)
                    self.car_coords.l_update(key, reset = 1)
                    if self.road.coords(self.cars[key][1].obj)[0] == -50:
                        self.road.move(self.cars[key][1].obj, 800, 0)
                        self.car_coords.l_update(key, reset = 1)

            # self.road.update()
            self.after_id = self.road.after(50, lambda: self.run())
        else:
            self.w.after_cancel(self.after_id)

class car_GUI:
    def __init__(self, c, img, x, y):
        self.img = (Image.open(img)).resize((100, 50), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.img)
        # c.photo = photo
        self.obj = c.create_image(x, y, image = self.photo)
    
c = cars()
app = environ(c)
tk.mainloop()
