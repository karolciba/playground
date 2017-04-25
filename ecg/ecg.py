#!/usr/bin/env python

import wfdb
import hmm
import numpy as np
import matplotlib.pyplot as plt
import pickle


def preprocess(count = 30):
    print("Preprocessing")
    sig, fields = wfdb.srdsamp('data/mitdb/100')

    ecg = sig[:500000,0]
    diff = np.diff(ecg)

    dmax = np.max(diff)-0.01
    dmin = np.min(diff)+0.01
    count = count - 2
    print(dmin,dmax)
    bins = [ dmin + (dmax - dmin)/count * i for i in range(count+1) ]
    print("bins",len(bins))
    quantized = np.digitize(diff, bins)

    dequant = np.empty(len(quantized))

    running = 0
    for i in range(len(dequant)):
        v = quantized[i]
        running += bins[v-1]
        dequant[i] = running

    return ecg,quantized,dequant,bins

def dequant(quantized, bins):
    dequant = np.empty(len(quantized))

    running = 0
    for i in range(len(dequant)):
        v = quantized[i]
        running += bins[v-1]
        dequant[i] = running

    return dequant

# def train():
#     print("Model training")
#     states = 10
#     model = hmm.random_model(states, count+2)
#
#     model = hmm.baum_welch(quantized, model)

def query():
    print("Questions answering")
    hmm.probabilities(model, 5)

def train():
    symbols = 50
    e, q, d, bins = preprocess(symbols)
    states = 50

    model = hmm.random_model(states,symbols)

    plt.ion()
    plt.subplot(211)
    plt.imshow(model.transitions)
    plt.subplot(212)
    plt.imshow(model.emissions)
    plt.show()
    plt.pause(0.001)

    i = 0
    # plt.savefig("out{}.png".format(i))

    # try:
    step=10000
    sig = q
    length = len(sig)
    fro = 0
    to = step

    print("\nIteration {}".format(i))
    while True:

        with open("db_ecg.pickle","wb") as pfile:
            pickle.dump(model,pfile)

        print("batch from {} to {}".format(fro,to),end="\r")

        i+=1
        if to >= length:
            print("\nIteration {}".format(i))
            fro = 0
            to = step


        obs = [ ]

        tmp_fro = fro
        tmp_to = to
        for x in range(8):
            obs.append(sig[tmp_fro:tmp_to])
            tmp_fro += step
            tmp_to += step

        fro += step
        to += step

        for o in obs:
            model = hmm.baum_welch(o,model)

        plt.subplot(211)
        plt.imshow(model.transitions)
        plt.subplot(212)
        plt.imshow(model.emissions)
        plt.show()
        plt.pause(0.001)
        plt.savefig("out{}.png".format(i))
    # except:
    #     pass

    plt.ioff()
    plt.subplot(211)
    plt.imshow(model.transitions)
    plt.subplot(212)
    plt.imshow(model.emissions)
    plt.show()

    return model, bins
