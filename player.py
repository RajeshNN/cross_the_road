class player:
    def __init__(self):
        self.posit = [0, 350]
    def update_lane(self, y):
        self.posit[0] = y
    def update_xpos(self, i):
        self.posit[1] = i