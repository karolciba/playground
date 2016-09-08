#!/usr/bin/env python
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np

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
    def marked_image(self):
        image = np.empty(self.image.shape + (3,), dtype="uint8")
        image[:,:,0] = np.copy(self.image)
        image[:,:,1] = np.copy(self.image)
        image[:,:,2] = np.copy(self.image)
        for key,value in self.pois.iteritems():
            image[value[0],value[1]] = [255,0,0]
        return image

def parse_file(filename):
    faces = []

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = reader.next()
        it = 0
        for line in reader:
            it += 1
            face = Face()
            for i in range(0,len(header)):
                face.set_poi(header[i],line[i])
            faces.append(face)
            # if it == 100:
                # break
            # break

    return faces

def visual(kohonen, width, heigh, window):
    v = np.ones( (width*(window+1), height*(window+1)) )*255
    v = v.astype('int')

    i = 0
    for row in kohonen._map:
        j = 0
        for col in row:
            im = col.reshape( (window,window) )
            im = im*255
            im = im.astype('int')
            v[i:i+window,j:j+window] = im
            j += window + 1
        i += window + 1

    print v

    # pltim.set_data(v)
    plt.imshow(v, cmap=plt.get_cmap("Greys_r"))
    plt.draw()
    plt.pause(0.1)
    # plt.imshow(v, cmap=plt.get_cmap("Greys_r"))
    # plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage %s file.csv" % (sys.argv[0], )

    filename = sys.argv[1]

    print "Parsing File"
    faces = parse_file(filename)
    f = faces[0]

    # plt.ion()
    plt.ioff()
    # plt.imshow(faces[0].image, cmap=plt.get_cmap("Greys_r"))
    # plt.show()
    import planar as p

    width = 10
    height = 10
    window = 9

    kohonen = p.Planar(window**2, (width,height))

    v = np.ones( (width*(window+1), height*(window+1)) )*255
    v = v.astype('int')

    # im = plt.imshow(v, cmap=plt.get_cmap("Greys_r"))
    # im = plt.imshow(v)

    print "Training"
    train = 0
    for f in faces:
        print "Train", train
        train += 1
        eye = f.poi_image('left_eye_inner_corner', window/2)
        # print eye
        # visual(kohonen, window, im)
        visual(kohonen, width, height, window)
        try:
            kohonen.train(eye.flatten()/255.)
        except:
            print "Soe error"

    print "Trainset", kohonen._train


    print "Visualizint"
    visual(kohonen, width, height, window)
    plt.show()
