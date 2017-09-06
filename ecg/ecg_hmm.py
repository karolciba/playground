#!/usr/bin/env python

# ideas:
# 0. negative delta in logprobability is not wrong - it means model is rebuilding
#    lower train signal probability is exchange for better distribution (?)
#    validate model change not logprob
#    after minus often returns to big pluses
# 1. init means with real signal (not much gain :(
# 2. start with small model and double after each convergence
# 3. find unprobable states and randomize them - to escape local minima ?
# 4. gradient descent/meadow path etc
# 5. reinforment? - find most probable for subsequence and strenghten it ?


import wfdb
# import hmm
import numpy as np
import matplotlib.pyplot as plt
import pickle

from hmmlearn import hmm
from hmmlearn import utils
from sklearn.externals import joblib


def preprocess(count = 30):
    print("Preprocessing")
    sig, fields = wfdb.srdsamp('data/mitdb/100')

    # ecg = sig[:500000,0]
    ecg = sig[:,0]
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

def latest_backup():
    import os
    import re

    files = os.listdir('.')
    pkl = [ f for f in files if re.match('model.*.pkl$',f) ]

    if not pkl:
        return None

    srt = sorted(pkl)
    f_name = srt[-1]

    print("Loading model", f_name)
    model = joblib.load(f_name)
    return model

def plot(model, symbols = 256, div = 4):
    symbols = 512
    eorig, q, d, bins = preprocess(symbols)

    eorig = eorig[0:500000]
    from scipy import signal
    # eorig = signal.resample(eorig, len(eorig))
    eorig = signal.decimate(eorig, div, ftype='fir')
    eorig = eorig[100:]
    eorig = np.diff(eorig)

    e = np.atleast_2d(eorig).T
    sube = np.atleast_2d(eorig[0:3000]).T

    plt.clf()
    plt.subplot(411)
    plt.imshow(model.transmat_,interpolation='nearest', shape=model.transmat_.shape)
    ax = plt.subplot(412)
    plt.plot(eorig[0:3000])
    plt.plot(np.cumsum(eorig[0:3000]))
    # plt.imshow(model.emissions,interpolation='nearest', shape=model.emissions.shape)
    plt.subplot(413, sharex = ax)
    plt.plot(model.predict(sube))
    plt.subplot(414, sharex = ax)
    samp = model.sample(3000)[0].flatten()
    plt.plot(samp)
    plt.plot(np.cumsum(samp))
    plt.show()
    plt.pause(1)

def double_model(model):

    symbols = model.n_components
    n_symbols = 2 * symbols

    n_model = hmm.GaussianHMM(n_components=n_symbols, verbose=True, min_covar=0.01, init_params='', n_iter = 10, covariance_type="diag")

    transmat_ = np.random.random((n_symbols,n_symbols))/100
    transmat_[0:symbols,0:symbols] = model.transmat_
    transmat_[symbols:n_symbols,symbols:n_symbols] = model.transmat_
    # unbalance it slightly
    transmat_ += np.random.random((n_symbols,n_symbols))/100
    n_model.transmat_ = transmat_
    utils.normalize(n_model.transmat_, 1)

    n_model.startprob_ = np.concatenate((model.startprob_, model.startprob_))
    utils.normalize(n_model.startprob_)
    n_model.means_ = np.concatenate((model.means_, model.means_))
    n_model._covars_ = np.concatenate((model._covars_, model._covars_))

    return n_model

def train(model = None):
    # backup: symbols = 128, div = 1
    # symbols = 128
    symbols = 4
    eorig, q, d, bins = preprocess(symbols)

    # eorig = eorig[0:500000]
    eorig = eorig[0:100000]
    # eorig = eorig[0:10000]
    from scipy import signal
    # eorig = signal.resample(eorig, len(eorig))
    eorig = signal.decimate(eorig, 8, ftype='fir')
    eorig = eorig[100:]
    eorig = np.diff(eorig)

    e = np.atleast_2d(eorig).T
    sube = np.atleast_2d(eorig[0:3000]).T

    # eps = np.finfo(np.float64).eps
    import sys
    eps = sys.float_info.min * symbols
    eps = 2e-290

    plt.ion()
    plt.clf()
    plt.plot(eorig[0:3000])
    # plt.subplot(311)
    # plt.imshow(model.transmat_,interpolation='nearest', shape=model.transitions.shape)
    # plt.subplot(312)
    # plt.imshow(model.,interpolation='nearest', shape=model.emissions.shape)
    # plt.subplot(313)
    # plt.plot(sampl)
    plt.show()
    plt.pause(1)

    if not model:
        model = hmm.GaussianHMM(n_components=symbols, verbose=True, min_covar=0.01, init_params='cs', n_iter = 10, covariance_type="diag")
        # left to right model, not staying in state but can jump to start

        # transmat_ = np.triu(np.random.random((symbols,symbols)),1)
        # transmat_[0,0] = 0
        # transmat_[:,0] = 1.0/symbols
        # model.transmat_ = transmat_
        # utils.normalize(model.transmat_, 1)

        transmat_ = np.random.random((symbols,symbols))/10
        # transmat_ += np.roll(np.eye(symbols),1,1)
        model.transmat_ = transmat_
        utils.normalize(model.transmat_, 1)

        # model.means_ = np.random.random((symbols,1))
        model.means_ = eorig[0:symbols].reshape(-1,1)
        # model.covars_ = np.random.random((symbols,1))
        # model = hmm.GMMHMM(n_components=symbols, verbose=True, n_iter = 10, covariance_type="full")
    else:
        plt.clf()
        plt.subplot(411)
        plt.imshow(model.transmat_,interpolation='nearest', shape=model.transmat_.shape)
        ax = plt.subplot(412)
        plt.plot(eorig[0:3000])
        # plt.imshow(model.emissions,interpolation='nearest', shape=model.emissions.shape)
        plt.subplot(413, sharex = ax)
        plt.plot(model.predict(sube))
        plt.subplot(414, sharex = ax)
        plt.plot(model.sample(3000)[0].flatten())
        plt.show()
        plt.pause(1)
        # model.transmat_[model.transmat_ <= eps] = eps
        # utils.normalize(model.transmat_, 1)

    import os
    import re
    files = os.listdir('.')
    pkl = [ f for f in files if re.match('model.*.pkl$',f) ]
    srt = sorted(pkl)

    i = len(srt)
    # plt.savefig("out{}.png".format(i))

    # try:


    print("\nIteration {}".format(i))
    while True:
        i += 1

        model.fit(e)
        model.init_params = ''
        joblib.dump(model, "model{:06d}.pkl".format(i))
        # print(model.transmat_)

        plt.clf()
        plt.subplot(411)
        plt.imshow(model.transmat_,interpolation='nearest', shape=model.transmat_.shape)
        ax = plt.subplot(412)
        plt.plot(eorig[0:3000])
        # plt.imshow(model.emissions,interpolation='nearest', shape=model.emissions.shape)
        plt.subplot(413, sharex = ax)
        plt.plot(model.predict(sube))
        plt.subplot(414, sharex = ax)
        samp = model.sample(3000)[0].flatten()
        plt.plot(samp)
        plt.plot(np.cumsum(samp))
        plt.show()
        plt.pause(0.001)
        plt.savefig("out{:06d}.png".format(i))

        hist = model.monitor_.history
        if abs(hist[0] - hist[1]) < 0.01:
            break

        # model.transmat_[model.transmat_ <= eps] = eps
        # utils.normalize(model.transmat_, 1)
    # except:
    #     pass


    return model
