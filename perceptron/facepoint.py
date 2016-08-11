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
        poi[0] = value
        self.pois[name] = poi
    def set_poi_y(self, name, value):
        poi = self.pois.get(name,[0,0])
        poi[1] = value
        self.pois[name] = poi
    def set_image(self, value, width=96, height=96):
        shape = (width, height)
        self.image = np.array(value.split()).astype('uint8').reshape(shape)


def parse_file(filename):
    faces = []

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = reader.next()
        for line in reader:
            face = Face()
            for i in range(0,len(header)):
                face.set_poi(header[i],line[i])
            faces.append(face)

    return faces

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage %s file.csv" % (sys.argv[0], )

    filename = sys.argv[1]

    faces = parse_file(filename)
