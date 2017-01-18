#!/usr/bin/env python
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
np.seterr(all='raise')
import random

class Face:
    def __init__(self):
        self.pois = {}
    def set_poi(self, name, value):
        if name.endswith("_x"):
            self.set_poi_x(name[:-2], value)
        elif name.endswith("_y"):
            self.set_poi_y(name[:-2], value)
        elif name == 'Image':
            self.set_image(value)
    def set_poi_x(self, name, value):
        poi = self.pois.get(name,[0,0])
        try:
            poi[1] = int(float(value))
        except:
            poi[1] = 0
        self.pois[name] = poi
    def set_poi_y(self, name, value):
        poi = self.pois.get(name,[0,0])
        try:
            poi[0] = int(float(value))
        except:
            poi[0] = 0
        self.pois[name] = poi
    def set_image(self, value, width=96, height=96):
        shape = (width, height)
        self.image = np.array(value.split()).astype('uint8').reshape(shape)
    def pois_names(self):
        return self.pois.keys()
    def poi_image(self,name,window):
        poi = self.pois[name]
        x = poi[0]
        y = poi[1]
        return self.image[x-window:x+window+1,y-window:y+window+1]
    def rand_image(self,window):
        x = random.randint(0+window,96-window)
        y = random.randint(0+window,96-window)
        return self.image[x-window:x+window+1,y-window:y+window+1]
    def marked_image(self):
        image = np.empty(self.image.shape + (3,), dtype="uint8")
        image[:,:,0] = np.copy(self.image)
        image[:,:,1] = np.copy(self.image)
        image[:,:,2] = np.copy(self.image)
        for key,value in self.pois.iteritems():
            image[value[0],value[1]] = [255,0,0]
        return image

def parse_file(filename, count = None):
    faces = []

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = reader.next()
        print "Available pois", header
        it = 0
        for line in reader:
            it += 1
            face = Face()
            for i in range(0,len(header)):
                face.set_poi(header[i],line[i])
            faces.append(face)
            if count and count == it:
                return faces
            # if it == 10:
            #     break
            # break

    return faces

def visual(kohonen, width, height, window, name=None):
    v = np.ones( (width*(window+1), height*(window+1)) )*255
    v = v.astype('int')

    # i = 0
    # for row in kohonen._map:
    #     j = 0
    #     for col in row:
    #         im = col.reshape( (window,window) )
    #         im = im*255
    #         im = im.astype('int')
    #         v[i:i+window,j:j+window] = im
    #         j += window + 1
    #     i += window + 1
    import scipy.misc

    for i in range(0,width):
        for j in range(0,height):
            col = kohonen._map[i,j]
            im = col.reshape( (window,window) )
            im = im*255
            im = im.astype('int')
            # v[i*(window+1):(i+1)*(window+1)-1,j*(window+1):(j+1)*(window+1)-1] = im
            xl = i*(window+1)
            xr = xl + window
            yl = j*(window+1)
            yr = yl + window
            v[xl:xr,yl:yr] = im
            # import pdb; pdb.set_trace()

    # scipy.misc.imsave(name+".png",v)
    scipy.misc.toimage(v,cmin=0,cmax=255).save(name+".png")

    # plt.imshow(v, cmap=plt.get_cmap("Greys_r"), interpolation='nearest')
    # # plt.draw()
    # # plt.pause(0.3)
    # if name:
    #     plt.savefig(name+".gif")
    # # plt.imshow(v, cmap=plt.get_cmap("Greys_r"))
    # # plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage %s file.csv" % (sys.argv[0], )

    filename = sys.argv[1]
    count = None
    if len(sys.argv) > 2:
        count = int(sys.argv[2])

    print "Parsing File"
    faces = parse_file(filename, count)
    f = faces[0]

    # plt.ion()
    plt.ioff()
    # plt.imshow(faces[0].image, cmap=plt.get_cmap("Greys_r"))
    # plt.show()
    import planar as p
    import random

    width = 50
    height = 50
    window = 15

    kohonen = p.Planar(window**2, (width,height))

    v = np.ones( (width*(window+1), height*(window+1)) )*255
    v = v.astype('int')

    # im = plt.imshow(v, cmap=plt.get_cmap("Greys_r"))
    # im = plt.imshow(v)

    print "Faces in database", len(faces)

    # print "Training with random"
    # train = 0
    # kohonen._delta = width/5
    # for f in faces:
    #     # for i in range(0,1):
    #     train += 1
    #     r = f.rand_image(window/2)
    #     try:
    #         kohonen.train(r.flatten()/255.)
    #     except:
    #         pass
    #     if train%100 == 0:
    #         print "\rTrain", train,
    #         sys.stdout.flush()
    #         visual(kohonen, width, height, window, "random"+str(train))

    print "\nTraining faces"
    train = 0
    kohonen._delta = 5

    import gc

    kohonen._delta = 3
    kohonen._coef = 0.01
    fcount = 0
    for i in range(5,0,-2):
        print "\nTrainset", i, "total", kohonen._train
        kohonen.delta(i)
        kohonen._coef = 0.01*i**2
        for f in faces:
            for poi_name in faces[0].pois_names():
                train += 1
                im = f.poi_image(poi_name, window/2)
                if im.shape != (window, window):
                    continue

                kohonen.train(im.flatten()/255.)

                if train%100 == 0:
                    # print "\rTrain", train, "gc", gc.collect(),
                    fcount += 1
                    print "\rTrain", train,
                    sys.stdout.flush()
                    fname = "face_%06d" % (fcount,)
                    visual(kohonen, width, height, window, fname)


    print "Visualizint"
    visual(kohonen, width, height, window, "finished")
    plt.show()
