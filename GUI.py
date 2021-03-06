import tkinter as tk
from random import randrange
from PIL import Image, ImageOps, ImageTk
import os
from cars import cars
from player import player

# setting up environment for the game
class environ:
    # initializing window, game play arena, coordinates for cars and player
    def __init__(self):
        self.w = tk.Tk(className = ' Cross The Road')
        self.cancel = False
        self.won = 0
        self.root = os.getcwd()
        self.right_img_files = ['redright.png', 'blueright.png', 'greenright.png']
        self.left_img_files = ['redleft.png', 'blueleft.png', 'greenleft.png']
        self.car_imgs = {}
        self.car_coords = cars()
        self.player = player()
        self.footpath1 = tk.Canvas(self.w, height = 50, width = 700, highlightbackground = 'black')
        self.footpath1.grid(row = 0, column = 0, rowspan = 1, columnspan = 1)
        self.color_footpath(self.footpath1, 7)
        self.road = tk.Canvas(self.w, height = 300, width = 700, bg = 'light blue', highlightbackground = 'black')
        self.road.grid(row = 1, column = 0, rowspan = 1, columnspan = 1)
        self.footpath2 = tk.Canvas(self.w, height = 50, width = 700, highlightbackground = 'black')
        self.footpath2.grid(row = 2, column = 0, rowspan = 1, columnspan = 1)
        self.color_footpath(self.footpath2, 7)
        self.panel = tk.Canvas(self.w, height = 300, width = 700, bg = 'light blue', highlightbackground = 'black')
        self.panel.grid(row = 3, column = 0, rowspan = 1, columnspan = 1)
        self.btn = tk.Button(self.panel, bg = 'SpringGreen2', text = 'Stop Game', font=('Helvetica 10 bold'), width = 10, height = 1, command = lambda: self.new_game())
        self.btn.grid(row = 0, column = 5, ipadx = 10)
        # coloring up the footpath
        x = 50
        l = []
        for i in range(5):
            l.append(self.road.create_line(0, x, 700, x, width = 3))
            x += 50
        # putting cars on the gameplay arena
        for j in self.car_coords.car_dict:
            f = randrange(3)
            if self.car_coords.car_dict[j][0] == 'r':
                p = os.path.join(self.root, 'right_cars', self.right_img_files[f])
                self.car_imgs[j] = ['r', self.draw_car(p, *self.car_coords.car_dict[j][1:3])]
            else:
                p = os.path.join(self.root, 'left_cars', self.left_img_files[f])
                self.car_imgs[j] = ['l', self.draw_car(p, *self.car_coords.car_dict[j][1:3])]
        # setting up player image
        self.pl = player_GUI(self.footpath2, self.player.posit[1], 25, os.path.join(self.root, 'chicken.png'))
        # binding arrow keys to window
        self.w.bind('<Left>', lambda q: self.left_key())
        self.w.bind('<Right>', lambda q: self.right_key())
        self.w.bind('<Up>', lambda q: self.up_key())
        self.w.bind('<Down>', lambda q: self.down_key())
        self.run()
    # defining functions for control keys
    def left_key(self):
        x1, y1 = self.pl.c.coords(self.pl.obj)
        if x1 > 20:
            self.pl.c.delete(self.pl.obj)
            self.pl.obj = self.pl.c.create_image(x1-30, y1, image = self.pl.mphoto)
            self.pl.r = 0
            self.player.update_xpos(x1-30)
    def right_key(self):
        x1, y1 = self.pl.c.coords(self.pl.obj)
        if x1 < 680:
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
            self.player.update_lane(int(y1/50) + 2)
    # defining functions to stop game
    def freeze(self):
        pass
    def call_to_freeze(self):
        self.w.bind('<Left>', lambda q: self.freeze())
        self.w.bind('<Right>', lambda q: self.freeze())
        self.w.bind('<Up>', lambda q: self.freeze())
        self.w.bind('<Down>', lambda q: self.freeze())
    def color_footpath(self, c, n):
        # called in __init__ to color the footpath
        h = int(c['height'])
        w = int(c['width'])
        for i in range(n):
            if i%2:
                c.create_rectangle(i*(w/n), 0, i*(w/n)+(w/n), h, fill = 'yellow')
            else:
                c.create_rectangle(i*(w/n), 0, i*(w/n)+(w/n), h, fill = 'black')
    # function to check collision of player with any of the cars
    def check_collision(self, lane, xpos):
        if lane:
            for car in self.car_coords.lane_dict[lane]:
                llim = self.car_coords.car_dict[car][1] - 50
                rlim = self.car_coords.car_dict[car][1] + 50
                if xpos+15>llim and xpos-15<rlim:
                    self.cancel = True
    def draw_car(self, img, a, b):
        # called to draw cars in __init__
        return car_GUI(self.road, img, a, b)
    # function to run the gameplay
    def run(self):
        if not self.cancel:
            for key in self.car_imgs:  # moving the cars
                if self.car_imgs[key][0] == 'r': # for right moving lanes
                    self.road.move(self.car_imgs[key][1].obj, 5, 0)
                    self.car_coords.r_update(key)
                    if self.road.coords(self.car_imgs[key][1].obj)[0] == 750:
                        self.road.move(self.car_imgs[key][1].obj, -800, 0)
                        self.car_coords.r_update(key, reset = 1)
                else:                            # for left moving lanes
                    self.road.move(self.car_imgs[key][1].obj, -5, 0)
                    self.car_coords.l_update(key)
                    if self.road.coords(self.car_imgs[key][1].obj)[0] == -50:
                        self.road.move(self.car_imgs[key][1].obj, 800, 0)
                        self.car_coords.l_update(key, reset = 1)
            self.check_collision(*self.player.posit) # checking collision after every iteration of car movement
            self.after_id = self.road.after(50, lambda: self.run())
        else:
            self.w.after_cancel(self.after_id)
            self.call_to_freeze()
            if self.won: # if game stopped by winning
                self.WO = self.road.create_text(350, 150, text = 'YOU WON!!!', font=('Helvetica 30 bold'), fill = 'white')
                self.BO = self.road.create_text(354, 154, text = 'YOU WON!!!', font=('Helvetica 30 bold'), fill = 'black')
                self.RO = self.road.create_text(352, 152, text = 'YOU WON!!!', font=('Helvetica 30 bold'), fill = 'red')
                self.btn.config(text = 'New Game')
            else: # if game stopped for any other reason
                self.WO = self.road.create_text(350, 150, text = 'GAME OVER\nYOU LOSE!!!', font=('Helvetica 30 bold'), fill = 'white')
                self.BO = self.road.create_text(354, 154, text = 'GAME OVER\nYOU LOSE!!!', font=('Helvetica 30 bold'), fill = 'black')
                self.RO = self.road.create_text(352, 152, text = 'GAME OVER\nYOU LOSE!!!', font=('Helvetica 30 bold'), fill = 'red')
                self.btn.config(text = 'New Game')
    # functions for button btn
    def new_game(self):
        if self.cancel == False:  # to stop the game when it's running
            self.cancel = True
            self.btn.config(text = 'New Game')
        else:                     # to start a new game when it's not running
            self.btn.config(text = 'Stop Game')
            self.cancel = False
            self.won = 0
            self.pl.c.delete(self.pl.obj)
            try:
                self.road.delete(self.WO, self.BO, self.RO)
            except:
                pass
            self.player = player()
            self.pl = player_GUI(self.footpath2, self.player.posit[1], 25, os.path.join(self.root, 'chicken.png'))
            self.w.bind('<Left>', lambda q: self.left_key())
            self.w.bind('<Right>', lambda q: self.right_key())
            self.w.bind('<Up>', lambda q: self.up_key())
            self.w.bind('<Down>', lambda q: self.down_key())
            self.run()
# function to prepare and manipulate car images
class car_GUI:
    def __init__(self, c, img, x, y):
        self.img = (Image.open(img)).resize((100, 50), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.img)
        self.obj = c.create_image(x, y, image = self.photo)
# function to prepare and manipulate player image
class player_GUI:
    def __init__(self, c, x, y, img):
        self.c = c
        self.r = 1
        self.img = Image.open(img).resize((30, 60), Image.ANTIALIAS)
        self.mimg = ImageOps.mirror(self.img)
        self.photo = ImageTk.PhotoImage(self.img)
        self.mphoto = ImageTk.PhotoImage(self.mimg)
        self.obj = c.create_image(x, y, image = self.photo)
# main function to start game instance
def main():
    app = environ()
    tk.mainloop()

if __name__ == "__main__":
    main()