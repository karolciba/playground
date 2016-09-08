#!/usr/bin/env python
import numpy as np
import matplotlib

# matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math


"""
Usage:

    som = Planar(3,20,10)
    ; set other parameters?
    for i in range(0,1000):
        som.train([red,green,blue])

    self.clasify([0.1,0.4,0.5])

"""
class Planar:
    def __init__(self, vector_size, map_size):
        self._length = vector_size
        self._width = map_size[0]
        self._height = map_size[1]

        self._map = np.random.random(map_size + (vector_size, ))
        self._train = 0
        self._coef = 0.2
        self._delta = 4

    def train(self, vector):
        self._train += 1

        bou_score = float('inf') # best maching unit
        bou_index = (0,0)
        for i in range(0, self._width):
            for j in range(0, self._height):
                score = 0
                score = math.sqrt( sum( (a - b)**2 for a,b in zip(vector,self._map[i,j])))
                if score < bou_score:
                    bou_score = score
                    bou_index = (i,j)

        min_x = max(bou_index[0] - self._delta, 0);
        max_x = min(bou_index[0] + self._delta, self._width)
        min_y = max(bou_index[1] - self._delta, 0);
        max_y = min(bou_index[1] + self._delta, self._height)

        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                for k in range(0, self._length):
                    self._map[i,j,k] -= self._coef * (self._map[i,j,k] - vector[k])
                    self._map[i,j,k] = max(self._map[i,j,k],0)
                    self._map[i,j,k] = min(self._map[i,j,k],1)

    def clasify(self, vector):
        pass


"""
Usage:

    som = Planar(3,20,10)
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
        self._im = plt.imshow(self._som._map)
        self._anim = []
    def show(self):
        # print "Show ", self._som
        self._im.set_data(self._som._map)
        self._anim.append( np.copy(self._som._map) )
        plt.draw()
        plt.pause(0.1)
    def animate(self):
        # print "Animate ", self._som
        # self.show()
        self._anim.append( np.copy(self._som._map) )
        # self._play()
    def _play(self):
        for i in self._anim:
            self._im.set_data(i)
            plt.draw()
            plt.pause(0.1)
    def save(self, filename):
        import matplotlib
        import matplotlib.animation
        fig = plt.figure()

        ims = []

        y = 0
        for i in self._anim:
            im = plt.imshow(i)
            # fname = "file%03d.png" % y
            # y+=1
            # plt.savefig(fname)
            ims.append( [im] )

        # Writer = matplotlib.animation.writers['ffmpeg']
        # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
        print ims

        im_ani = matplotlib.animation.ArtistAnimation(fig, ims)
        # im_ani.save('im.mp4', writer=writer)
        im_ani.save('im.mp4')






if __name__ == "__main__":
    som = Planar(3, (200,200))
    vis = Visualizer(som)
    vis.animate()
    print ""

    for i in range(0,10000):
        if (i%10 == 0):
            print "Train no ", i
            vis.show()
        vector = np.random.random(3)

        som.train(vector)

    vis.save('foobar')

    # try:
    #     while True:
    #         vis.animate()
    # except KeyboardInterrupt:
    #     pass
