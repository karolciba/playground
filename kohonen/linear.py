#!/usr/bin/env python
import numpy as np
import matplotlib

# matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import math
import scipy.signal

class Linear:
    def __init__(self, vector_size, map_size):
        self._length = vector_size
        self._size = map_size

        # self._map = np.zeros( (map_size, vector_size) )
        # self._map = np.random.random( (map_size, vector_size) )
        self._map = np.random.normal(0.0,0.01, (map_size, vector_size) )
        # self._map[0] = np.zeros(vector_size)
        # self._map[map_size-1] = np.ones(vector_size)

        # self._map[:] = [0, 0]

        # self._map = np.empty( (map_size, vector_size ) )

        self._train = 0
        self._coef = 0.01
        self._delta = map_size/10
        self._sim = scipy.signal.ricker(self._delta, (self._delta-1)/2)
        self._sim /= np.max(self._sim)
        # self._sim = scipy.signal.gaussian(self._delta, self._delta/4)
        # self._sim = scipy.signal.flattop(self._delta)

    def train(self, vector):

        self._train += 1

        bou_score = float('inf')
        bou_index = 0
        # for i in range(0, self._size):
        #     score = math.sqrt( sum( (a - b)**2 for a,b in zip(vector,self._map[i])))
        #     if score < bou_score:
        #         bou_score = score
        #         bou_index = i

        # find best matching unit
        score_matrix =  np.linalg.norm(self._map-vector,axis=1)
        bou_index = np.argmin(score_matrix)

        # min_x = max(bou_index - self._delta, 0)
        # max_x = min(bou_index + self._delta, self._size)
        min_x = bou_index - self._delta
        max_x = bou_index + self._delta

        for n in range(min_x, max_x):
            if n < 0:
                i = self._size + n
                # print "less", n, i
            elif n >= self._size:
                i = (n % self._size) - 1
                # print "more", n, i
            else:
                i = n

            dist = abs(bou_index - n)
            sim = self._sim[dist - 1]

            if i == bou_index and (self._train % 100 == 0):
                print n, i, bou_index, dist, sim, vector, self._map[i],


            # sim = abs(dist/float(self._delta))
            for k in range(0, self._length):
                # distance = math.sqrt( sum( (a - b)**2 for a,b in zip(vector,self._map[i])))
                # self._map[i,k] -= self._coef * distance
                self._map[i,k] -= sim * self._coef * (self._map[i,k] - vector[k])
                # self._map[i,k] = max(self._map[i,k], 0)
                # self._map[i,k] = min(self._map[i,k], 1)


"""
Usage:

    som = Kohonen(3,20,10)
    vis = Visualizer(som)

    som.train([red,green,blue])
    vis.show()

    for i in range(0,1000):
        som.train([red,green,blue])
        vis.animate()

"""
class Visualizer:
    def __init__(self, kohonen):
        self._som = kohonen
        # plt.ion()
        # self._im = plt.imshow(self._som._map)
        self._anim = []
        self._ims = []
        self._fig = plt.figure()
        self._ax = self._fig.add_subplot(111)
        self._codes = np.empty(self._som._size)
        self._codes[0:self._som._size-1] = Path.LINETO
        self._codes[0] = Path.MOVETO
        self._codes[-1] = Path.STOP
        # self._codes[-1] = Path.CLOSEPOLY

    def show(self):
        # print "Show ", self._som
        # self._im.set_data(self._som._map)
        # self._anim.append( np.copy(self._som._map) )

        path = Path(self._som._map, self._codes)
        patch = patches.PathPatch(path, facecolor='none', lw=1)

        self._ims.append(patch)

        self._ax.add_patch(patch)

        plt.draw()
        plt.pause(0.1)
        # plt.show()
        # plt.draw()
        # plt.pause(0.1)
    def animate(self):
        print "Animate ", self._som
        self.show()
        self._anim.append( np.copy(self._som._map) )
        self._play()
    def _play(self):
        for i in self._anim:
            self._im.set_data(i)
            plt.draw()
            plt.pause(0.1)

    def save(self, filename):
        import matplotlib
        import matplotlib.animation
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ims = self._ims
        def anim(num):
            ax.add_patch(ims[num])
            plt.clf()

        # im_ani = matplotlib.animation.ArtistAnimation(fig, anim, frames=len(ims))
        im_ani = matplotlib.animation.FuncAnimation(fig, anim, frames=len(ims))
        # im_ani.save('im.mp4', writer=writer)
        im_ani.save('im.mp4')






if __name__ == "__main__":
    som = Linear(2, 900)
    vis = Visualizer(som)
    # vis.animate()
    print ""

    sign = lambda x: (1, -1)[x<0]
    import math
    signs = [-1,1]

    # for i in range(0,10000):
    i = 0
    while True:
    # for i in range(0,100):
        i+=1
        if (i%100 == 0):
            print "Train no ", i
            vis.show()
            print vector
            # print som._map[0:20]
        # vector = np.random.random(2)
        # x = np.random.random()

        x = np.random.uniform(0,0.5)
        ysq = 0.5**2 - x**2
        y = math.sqrt(ysq)

        xsn = signs[np.random.randint(0,2)]
        ysn = signs[np.random.randint(0,2)]
        shx = 0.5 + np.random.normal(0,0.01)
        shy = 0.5 + np.random.normal(0,0.01)
        vector = [xsn*x+shx, ysn*y+shy]

        # print vector, math.sqrt(x**2+y**2)

        som.train(vector)

    vis.save('foobar')

    # try:
    #     while True:
    #         vis.animate()
    # except KeyboardInterrupt:
    #     pass
