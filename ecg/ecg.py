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

    emax = np.max(ecg)
    emin = np.min(ecg)
    count = count - 2
    bins = [ emin + (emax - emin)/count * i for i in range(count+1) ]
    quantized = np.digitize(ecg, bins)
    dequant = np.empty(len(quantized))

    # dmax = np.max(diff)-0.01
    # dmin = np.min(diff)+0.01
    # count = count - 2
    # print(dmin,dmax)
    # bins = [ dmin + (dmax - dmin)/count * i for i in range(count+1) ]
    # print("bins",len(bins))
    # quantized = np.digitize(diff, bins)
    #
    # dequant = np.empty(len(quantized))

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
    symbols = 100
    states = 30
    e, q, d, bins = preprocess(symbols)

    model = hmm.random_model(states,symbols)
    gen = hmm.synthetic(model)
    sampl = [next(gen) for _ in range(1000)]

    plt.ion()
    plt.clf()
    plt.subplot(311)
    plt.imshow(model.transitions,interpolation='nearest', shape=model.transitions.shape)
    plt.subplot(312)
    plt.imshow(model.emissions,interpolation='nearest', shape=model.emissions.shape)
    plt.subplot(313)
    plt.plot(sampl)
    plt.show()
    plt.pause(0.001)

    i = 0
    plt.savefig("out{}.png".format(i))

    # try:
    step = 10000
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
        if to >= length - 9*step:
            print("\nIteration {}".format(i))
            fro = 0
            to = step


        obs = [ ]

        # tmp_fro = fro
        # tmp_to = to
        # for x in range(8):
        #     obs.append(sig[tmp_fro:tmp_to])
        #     tmp_fro += step
        #     tmp_to += step
        o = sig[fro:to]

        fro += step
        to += step

        # for o in obs:
        #     model = hmm.baum_welch(o,model)
        for i in range(100):
            model = hmm.baum_welch(o,model)

        gen = hmm.synthetic(model)
        sampl = [next(gen) for _ in range(1000)]
        # model = hmm.batch_baum_welch(obs,model)

        plt.clf()
        plt.subplot(311)
        plt.imshow(model.transitions,interpolation='nearest', shape=model.transitions.shape)
        plt.subplot(312)
        plt.imshow(model.emissions,interpolation='nearest', shape=model.emissions.shape)
        plt.subplot(313)
        plt.plot(sampl)
        plt.show()
        plt.pause(0.001)
        plt.savefig("out{}.png".format(i))
    # except:
    #     pass

    plt.ioff()
    plt.subplot(311)
    plt.imshow(model.transitions,interpolation='nearest', shape=model.transitions.shape)
    plt.subplot(312)
    plt.imshow(model.emissions,interpolation='nearest', shape=model.emissions.shape)
    plt.subplot(313)
    plt.plot(sampl)
    plt.show()

    return model, bins
