import numpy as np
import time
import sys
import tkinter as tk

UNIT = 10  # pixels
MAZE_H = 15  # grid height
MAZE_W = 15  # grid width

class Plane(tk.Tk, object):
    def __init__(self):
        super(Plane, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.n_features = 2
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
        # return observation QLearning
        # return self.canvas.coords(self.rect)
        # return observation DQN
        nearest = np.array(self.canvas.coords(self.rect)[:2])
        minimum = 99999
        for coord in self.hits:
            dist = abs(np.sum(np.array(self.canvas.coords(self.rect)[:2]) - np.array(self.canvas.coords(coord)[:2])))
            if dist == 0:
                self.canvas.create_rectangle(self.canvas.coords(coord), fill='yellow')
                self.canvas.delete(coord)
                remove=coord
            elif dist < minimum:
                minimum = dist
                nearest = coord
        self.hits.remove(remove)
        return (np.array(self.canvas.coords(self.rect)[:2]) - np.array(self.canvas.coords(nearest)[:2])) / (MAZE_H * UNIT)

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

        next_coords = self.canvas.coords(self.rect)  # next state

        # reward function
        coordsObj = {}
        for coord in self.hits:
            coordsObj.update({str(self.canvas.coords(coord)):coord} )

        if str(next_coords) in coordsObj.keys():
            reward = 10
            self.canvas.delete(coordsObj.get(str(next_coords)))
            self.canvas.create_rectangle(next_coords,fill='yellow')
            self.hits.remove(coordsObj.get(str(next_coords)))
            if len(self.hits) == 0:
                done = True
                # #QLearning
                # next_coords = 'terminal'
            else:
                done = False
        else:
            reward = -1
            done = False
        #DQN
        if not done:
            nearest = np.array([0,0])
            minimum = 99999
            for coord in self.hits:
                dist = np.sum(np.array(next_coords[:2]) - np.array(self.canvas.coords(coord)[:2]))
                if dist < minimum:
                    minimum = dist
                    nearest = coord
            s_ = (np.array(next_coords[:2]) - np.array(self.canvas.coords(nearest)[:2]))/(MAZE_H*UNIT)
        else:
            s_ = next_coords[:2]
        return s_, reward, done
        # #QLearning
        # return next_coords,reward, done

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
    env = Plane().__init__()
    env.after(200, update)
    env.mainloop()