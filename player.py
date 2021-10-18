class player:
    def __init__(self):
        self.posit = [0, 335]
        self.canv_flag = 0
    def update_lane(self, y):
        if self.canv_flag:
            self.posit[0] = y
    def update_xpos(self, i):
        self.posit[1] = i