import numpy as np
import time
import sys
import tkinter as tk

UNIT = 50  # pixels
MAZE_H = 3  # grid height
MAZE_W = 3  # grid width

class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('panel')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        self.draw()

        # pack all
        self.canvas.pack()

    def draw(self):
        # create origin
        origin = np.array([UNIT / 2, UNIT / 2])

        # create dots according given function
        self.hits = []
        for i in range(0, MAZE_W * UNIT, UNIT):
            y = i
            if y >= MAZE_H * UNIT:
                continue
            hit_center = origin + np.array([i, round(y)])
            hit = self.canvas.create_rectangle(
                hit_center[0] - (UNIT / 2 - 2), hit_center[1] - (UNIT / 2 - 2),
                hit_center[0] + (UNIT / 2 - 2), hit_center[1] + (UNIT / 2 - 2),
                fill='black')
            self.hits.append(hit)

        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - (UNIT / 2 - 2), origin[1] - (UNIT / 2 - 2),
            origin[0] + (UNIT / 2 - 2), origin[1] + (UNIT / 2 - 2),
            fill='red')

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        self.draw()
        # return observation
        return self.canvas.coords(self.rect)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.rect)  # next state

        # reward function
        coordsObj = {}
        for coord in self.hits:
            coordsObj.update({str(self.canvas.coords(coord)):coord} )
        if str(s_) in coordsObj.keys():
            reward = 10
            self.canvas.delete(coordsObj.get(str(s_)))
            self.canvas.create_rectangle(s_,fill='yellow')
            self.hits.remove(coordsObj.get(str(s_)))
            if len(self.hits) == 0:
                done = True
                s_ = 'terminal'
            else:
                done = False
        else:
            reward = -1
            done = False
        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()


def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s,r, done = env.step(a)
            if done:
                break

if __name__ == '__main__':
    function=sys.argv[0]
    env = Maze().__init__()
    env.after(100, update)
    env.mainloop()