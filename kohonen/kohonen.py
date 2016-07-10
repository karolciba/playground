#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt


"""
Usage:

    som = Kohonen(3,20,10)
    ; set other parameters?
    for i in range(0,1000):
        som.train([red,green,blue])

    self.clasify([0.1,0.4,0.5])

"""
class Kohonen:
    def __init__(self, vector_size, map_size):
        self._length = vector_size
        self._width = map_size[0]
        self._height = map_size[1]

        self._map = np.random.random(map_size + (vector_size, ))
        self._train = 0
        self._coef = 0.1
        self._delta = 10

    def train(self, vector):
        # print "vector", vector

        self._train += 1

        bou_score = 0 # best maching unit
        bou_index = (0,0)
        for i in range(0, self._width):
            for j in range(0, self._height):
                score = 0
                for k in range(0, self._length):
                    score += (self._map[i,j,k] - vector[k])**2
                if score > bou_score:
                    bou_score = score
                    bou_index = (i,j)

        # print "best matching", bou_index, bou_score
        # print self._map[bou_index]

        min_x = max(bou_index[0] - self._delta, 0);
        max_x = min(bou_index[0] + self._delta, self._width-1)
        min_y = max(bou_index[1] - self._delta, 0);
        max_y = min(bou_index[1] + self._delta, self._height-1)

        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                for k in range(0, self._length):
                    # print "before", self._map[i,j,k]
                    self._map[i,j,k] -= self._coef * (self._map[i,j,k] - vector[k])
                    # print "after", self._map[i,j,k]
                    self._map[i,j,k] = max(self._map[i,j,k],0)
                    self._map[i,j,k] = min(self._map[i,j,k],1)
        # print self._map[bou_index]


        """
        el_a = self._map - vector

        el_square = np.multiply(el_a, el_a)

        el_sum = np.sum(el_square, axis=2)

        max_elem = np.argmax(el_sum)

        max_ind = np.unravel_index(max_elem, el_sum.shape)

        coef = [ 0.01, 0.01, 0.01 ]

        delta = 10

        min_x = max(max_ind[0] - delta, 0);
        max_x = min(max_ind[0] + delta, self._map.shape[0]-1)
        min_y = max(max_ind[1] - delta, 0);
        max_y = min(max_ind[1] + delta, self._map.shape[1]-1)

        map_slice = self._map[ min_x:max_x, min_y:max_y]
        # print map_slice
        # print self._map[max_ind]
        map_slice += coef * (vector - map_slice)
        print map_slice[ map_slice > 1]
        import pdb; pdb.set_trace()
        map_slice[ map_slice > 1.0] = 1.0
        map_slice[ map_slice < 0.0] = 0.0
        # print map_slice
        # print self._map[max_ind]

        # print "max index ", max_ind
        """

    def clasify(self, vector):
        pass


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
        plt.ion()
        self._im = plt.imshow(self._som._map)
    def show(self):
        # print "Show ", self._som
        self._im.set_data(self._som._map)
        plt.draw()
        plt.pause(0.1)
    def animate(self):
        # print "Animate ", self._som
        self.show()




if __name__ == "__main__":
    som = Kohonen(3, (200,200))
    vis = Visualizer(som)
    vis.animate()
    print ""

    for i in range(0,10000):
        if (i%10 == 0):
            print "Train no ", i
            vis.animate()
        vector = np.random.random(3)

        som.train(vector)
