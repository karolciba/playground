#!/usr/bin/env python
#
# changes to hmmlearn:
# 0. negative delta doesnt end 
# 1. prevent overfitting by not allowing for setting transition prob to 0

# ideas:
# 0. negative delta in logprobability is not wrong - it means model is rebuilding
#    lower train signal probability is exchange for better distribution (?)
#    validate model change not logprob
#    after minus often returns to big pluses
# 1. init means with real signal (not much gain :(
# 2. start with small model and double after each convergence (something positive)
# 3. find unprobable states and randomize them - to escape local minima ?
#    3.1 change least unprobable states (not used in pred) and change for best matched
#        - in naive way (replace row, replace mean, max covar from existing)
#        doesnt work.
#    3.2 replace not used states to random state from used-ones (weighted?) and
#        fix transitions to those to states - setting them to 1/2 of original
#        slightly moving away means (by 10%?)
#    3.3 do not fix unused for small nets or/and when states have similar transitions
#        for small nets whole model seems like Gaussian Mixture in disguise
#        for similar transitions change seems not doing anything good
#    3.4 fix issues with convergence (consider negative delta?)

# 4. gradient descent/meadow path etc
# 5. reinforment? - find most probable for subsequence and strenghten it ?
#    which is attempt to minimize -> argmin Var( P(state | model, data ) in function of model
#    trying to maximize information density carried by model, in attemp to
#    achieve each state utilization equal


import wfdb
# import hmm
import numpy as np
import matplotlib.pyplot as plt
import pickle

from hmmlearn import hmm
from hmmlearn import utils
from sklearn.externals import joblib


def preprocess(decimation = 8):
    print("Preprocessing")
    sig, fields = wfdb.srdsamp('data/mitdb/100')

    # ecg = sig[:500000,0]
    ecg = sig[:,0]

    from scipy import signal
    # eorig = signal.resample(eorig, len(eorig))
    if decimation != 0:
        ecg = signal.decimate(ecg, decimation, ftype='fir')

    diff = np.diff(ecg)

    cum = 0
    filtered = np.empty_like(ecg)
    for i in range(len(diff)):
        cum *= 0.9
        cum += diff[i]
        filtered[i] = cum

    return ecg[:-1],diff,filtered[:-1]

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

def plot(model, div = 8):
    ecg, diff, filt = preprocess(div)

    # e = np.atleast_2d(eorig).T
    # sube = np.atleast_2d(eorig[0:3000]).T
    e = diff[:10000].reshape(-1,1)
    # e = np.column_stack((diff,filt))
    sube = e[:3000]

    plt.clf()
    plt.subplot(411)
    plt.imshow(model.transmat_,interpolation='nearest', shape=model.transmat_.shape)
    ax = plt.subplot(412)
    plt.plot(e[0:3000])
    plt.plot(ecg[:3000])
    # plt.imshow(model.emissions,interpolation='nearest', shape=model.emissions.shape)
    plt.subplot(413, sharex = ax)
    model.algorithm = 'viterbi'
    plt.plot(model.predict(sube))
    model.algorithm = 'map'
    plt.plot(model.predict(sube))
    plt.subplot(414, sharex = ax)
    samp = model.sample(3000)[0]
    plt.plot(samp)
    plt.plot(np.cumsum(samp[:,0]))
    plt.show()
    plt.pause(1)

def model_plot(model):
    plt.clf()
    plt.subplot(121)
    plt.imshow(model.transmat_)
    plt.subplot(122)
    plt.plot(model.means_.flatten())
    plt.plot(model.covars_.flatten())
    plt.show()
    plt.pause(1)

def diff_plot(model,previous):
    plt.clf()
    ax = plt.subplot(221)
    plt.imshow(model.transmat_)
    plt.subplot(222, sharex = ax, sharey = ax)
    plt.imshow(model.transmat_ - previous.transmat_)
    ax = plt.subplot(223)
    plt.plot(model.means_)
    plt.plot(model.means_ - previous.means_)
    plt.subplot(224, sharex = ax)
    plt.plot(model._covars_)
    plt.plot(model._covars_ - previous._covars_)

def states_plot(model,div=8):
    ecg, diff, filt = preprocess(div)

    # e = np.atleast_2d(eorig).T
    # sube = np.atleast_2d(eorig[0:3000]).T
    e = diff[:3000].reshape(-1,1)

    logprob, posterior = model.score_samples(e)

    plt.clf()
    ax = plt.subplot(211)
    plt.plot(e)
    plt.subplot(212,sharex=ax)
    plt.imshow(posterior.T, aspect='auto')


def usage_plot(model,div=8):
    ecg, diff, filt = preprocess(div)

    # e = np.atleast_2d(eorig).T
    # sube = np.atleast_2d(eorig[0:3000]).T
    e = diff[:10000].reshape(-1,1)

    logprob, posterior = model.score_samples(e)
    usage = np.sum(posterior.T,axis=1)

    # plt.clf()
    plt.plot(np.sort(usage)/float(sum(usage)))

def clone_model(model):
    from sklearn.externals import joblib
    joblib.dump(model,"/tmp/foobarmodel.pkl")
    return joblib.load("/tmp/foobarmodel.pkl")

def double_model(model):

    symbols = model.n_components
    n_symbols = 2 * symbols

    n_model = hmm.GaussianHMM(n_components=n_symbols, verbose=True, min_covar=0.01, init_params='', n_iter = model.n_iter, covariance_type="diag", tol=model.tol)

    transmat_ = np.random.random((n_symbols,n_symbols))/1000
    transmat_[0:symbols,0:symbols] = model.transmat_
    transmat_[symbols:n_symbols,symbols:n_symbols] = model.transmat_
    # unbalance it slightly
    transmat_ += np.random.random((n_symbols,n_symbols))/1000
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
    symbols = 1024
    div = 8
    ecg, diff, filt = preprocess(div)

    # e = np.atleast_2d(eorig).T
    # sube = np.atleast_2d(eorig[0:3000]).T
    # e = np.column_stack((diff,filt))
    e = diff[:10000].reshape(-1,1)
    sube = e[:3000]

    # eps = np.finfo(np.float64).eps
    import sys
    eps = sys.float_info.min * symbols
    eps = 2e-290

    plt.ion()
    plt.clf()
    plt.plot(e[0:3000])
    # plt.subplot(311)
    # plt.imshow(model.transmat_,interpolation='nearest', shape=model.transitions.shape)
    # plt.subplot(312)
    # plt.imshow(model.,interpolation='nearest', shape=model.emissions.shape)
    # plt.subplot(313)
    # plt.plot(sampl)
    plt.show()
    plt.pause(1)

    if not model:
        model = hmm.GaussianHMM(n_components=symbols, verbose=True, min_covar=0.01, init_params='cmts', n_iter = 100, tol = 1, covariance_type="diag")
        # left to right model, not staying in state but can jump to start

        # transmat_ = np.triu(np.random.random((symbols,symbols)),1)
        # transmat_[0,0] = 0
        # transmat_[:,0] = 1.0/symbols
        # model.transmat_ = transmat_
        # utils.normalize(model.transmat_, 1)

        # transmat_ = np.random.random((symbols,symbols))/10
        # # transmat_ += np.roll(np.eye(symbols),1,1)
        # model.transmat_ = transmat_
        # utils.normalize(model.transmat_, 1)

        # model.means_ = np.random.random((symbols,1))
        # model.means_ = e[0:symbols].reshape(-1,1)
        # model.covars_ = np.random.random((symbols,1))
        # model = hmm.GMMHMM(n_components=symbols, verbose=True, n_iter = 10, covariance_type="full")
    else:
        plot(model, div)

    import os
    import re
    files = os.listdir('.')
    pkl = [ f for f in files if re.match('model.*.pkl$',f) ]
    srt = sorted(pkl)

    i = len(srt)
    # plt.savefig("out{}.png".format(i))

    # try:


    best_model = clone_model(model)
    best_score = -999999999999.0
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
        plt.plot(e[0:3000])
        # plt.imshow(model.emissions,interpolation='nearest', shape=model.emissions.shape)
        plt.subplot(413, sharex = ax)
        plt.plot(model.predict(sube))
        plt.subplot(414, sharex = ax)
        samp = model.sample(3000)[0]
        plt.plot(samp)
        plt.plot(np.cumsum(samp[:,0]))
        plt.show()
        plt.pause(0.001)
        plt.savefig("out{:06d}.png".format(i))

        # score = model.monitor_.history[1]
        # if score > best_score:
        #     print("Found better {} than {}, switching".format(score,best_score))
        #     best_score = score
        #     best_model = clone_model(model)
        # else:
        #     model = best_model

        # hist = model.monitor_.history
        # if abs(hist[0] - hist[1]) < 0.01:
        #     break

        fix_unused(model,e)

        # model.transmat_[model.transmat_ <= eps] = eps
        # utils.normalize(model.transmat_, 1)
    # except:
    #     pass


    return model

def recursive_train(model = None):
    while True:
        model = train(model)
        print("doubling model",model.n_components)
        model = double_model(model)

def reorder_usage(model, div = 8):
    ecg, diff, filt = preprocess(div)

    e = diff[:10000].reshape(-1,1)

    logprob, posterior = model.score_samples(e)
    usage = np.sum(posterior.T,axis=1)
    keys = np.flip(np.argsort(usage),axis=0)

    model.means_ = model.means_[keys]
    model._covars_ = model._covars_[keys]
    model.startprob_ = model.startprob_[keys]

    model.transmat_ = model.transmat_[keys]
    model.transmat_[:,:] = model.transmat_[:,keys]

def reorder_model(model, div = 8):
    ecg, diff, filt = preprocess(div)

    # e = np.atleast_2d(eorig).T
    # sube = np.atleast_2d(eorig[0:3000]).T
    e = diff[:10000].reshape(-1,1)
    # e = np.column_stack((diff,filt))
    # sube = e[:3000]

    pred = model.predict(e)
    bc = np.bincount(pred,minlength=model.n_components)

    keys = np.flip(np.argsort(bc),axis=0)

    model.means_ = model.means_[keys]
    model._covars_ = model._covars_[keys]
    model.startprob_ = model.startprob_[keys]


    model.transmat_ = model.transmat_[keys]
    model.transmat_[:,:] = model.transmat_[:,keys]


def fix_unused(model, signal):
    # """Unused states decided MAP or viterbi usage"""
    # model.algorithm = 'map'
    # pred = model.predict(signal)
    # usage = np.bincount(pred,minlength=model.n_components)
    # treshold = np.sort(usage)[model.n_components//10]
    #
    # ids = np.argwhere(usage <= treshold).flatten()
    # used = np.argwhere(usage > treshold).flatten()
    # probs = usage/float(sum(usage))

    # """Unused states decided on average state probability"""
    # logprob, posterior = model.score_samples(signal)
    # usage = np.sum(posterior.T,axis=1)
    # treshold = np.sort(usage)[model.n_components//10]
    # ids = np.argwhere(usage <= treshold).flatten()
    # used = np.argwhere(usage > treshold).flatten()
    #
    # probs = usage/float(sum(usage))


    """Unused states decided on average state probability"""
    logprob, posterior = model.score_samples(signal)
    usage = np.sum(posterior.T,axis=1)
    # treshold = np.sort(usage)[model.n_components//10]
    # ids = np.argwhere(usage <= treshold).flatten()
    # used = np.argwhere(usage > treshold).flatten()
    probs = usage/float(sum(usage))
    ids = np.argwhere(probs <= 0.001).flatten()
    used = np.argwhere(probs > 0.001).flatten()

    mapped = {}
    # model.algorithm = 'map'

    import random
    import sklearn.mixture

    print("There are {} used and {} unsued".format(len(used),len(ids)))

    ids = ids[0:len(used)]
    print("After clipping there are {} used and {} unused".format(len(used),len(ids)))

    for id in ids:
        # replace_id = np.random.choice(used)
        # randomly select node to clone according to its "information weight"
        # replace_id = np.random.choice(model.n_components,p=probs)
        replace_id = random.choices(range(model.n_components),weights=probs)[0]

        mapped[id] = [replace_id, int(probs[id]*1000)/1000, int(probs[replace_id]*1000)/1000, int(model.transmat_[replace_id,replace_id]*1000)/1000]



        # if (np.sum(model.transmat_[:,replace_id])) > 3):
        # unroll thight self loop
        if model.transmat_[replace_id,replace_id] > 0.1:
            # can clone this state any more
            probs[replace_id] = 0
            probs[id] = probs[replace_id]

            mapped[id].append('s')
            in_trans = model.transmat_[:,id].copy()
            model.transmat_[id,:] = model.transmat_[replace_id,:]
            model.transmat_[replace_id,id] += model.transmat_[replace_id,replace_id]
            model.transmat_[id,id] += model.transmat_[replace_id,replace_id]
            model.transmat_[replace_id,replace_id] = 2e-290

            # staing in giver state is forbidden
            # in place of that transit to cloned state
            # model.transmat_[replace_id,id] += model.transmat_[replace_id,replace_id]
            # model.transmat_[replace_id,replace_id] = 0.0001
            utils.normalize(model.transmat_, 1)

            model.startprob_[replace_id] /= 2.
            model.startprob_[id] += model.startprob_[replace_id]

            model.means_[id] = model.means_[replace_id]
            # diverge them slighly to cover more ground
            # model.means_[replace_id] *= 1.001
            model._covars_[id] = model._covars_[replace_id]
        #TODO: unroll longer loops

        #refit to general node
        # to many ins, to many out, to large emission - coverage
        elif random.random() > 0.5:
            # lower prob of used node
            # allow cloning of both
            probs[replace_id] /= 2
            probs[id] = probs[replace_id]

            size = model.n_components
            ord = np.random.binomial(1,0.5,model.n_components)
            nord = 1 - ord

            mapped[id].append('i')
            in_trans = model.transmat_[:,id].copy()
            # clone the not used node
            # out transitions (row) like in original
            model.transmat_[id,:] = model.transmat_[replace_id,:]

            # in trasitions (column) half for each of two (original and clone)
            model.transmat_[:,id][ord == 1] = model.transmat_[:,replace_id][ord == 1]
            model.transmat_[:,id][ord == 0] = 2e-290
            model.transmat_[:,replace_id][ord == 1] = 2e-290

            # original trans should be small, add to them to keep row normalization to 1
            utils.normalize(model.transmat_, 1)

            model.startprob_[replace_id] /= 2.
            model.startprob_[id] += model.startprob_[replace_id]

            model.means_[id] = model.means_[replace_id]
            model._covars_[id] = model._covars_[replace_id]
        else:
            # lower prob of used node
            # allow cloning of both
            probs[replace_id] /= 2
            probs[id] = probs[replace_id]

            size = model.n_components
            ord = np.random.binomial(1,0.5,model.n_components)
            nord = 1 - ord

            mapped[id].append('o')
            in_trans = model.transmat_[:,id].copy()
            # clone the not used node
            # out transitions (row) like in original
            model.transmat_[id,:][ord == 1] = model.transmat_[replace_id,:][ord == 1]
            model.transmat_[id,:][ord == 0] = 2e-290
            model.transmat_[replace_id,:][ord == 1] =  2e-290

            # in trasitions (column) half for each of two (original and clone)
            model.transmat_[:,replace_id] /= 2.
            model.transmat_[:,id] = in_trans/2. + model.transmat_[:,replace_id]
            # model.transmat_[:,replace_id] += in_trans/2.

            # original trans should be small, add to them to keep row normalization to 1
            utils.normalize(model.transmat_, 1)

            model.startprob_[replace_id] /= 2.
            model.startprob_[id] += model.startprob_[replace_id]

            model.means_[id] = model.means_[replace_id]
            model._covars_[id] = model._covars_[replace_id]

    print("fixed no nodes",len(ids), mapped)

def fix_unused_to_big_covar(model, signal):
    pred = model.predict(signal)
    bc = np.bincount(pred,minlength=model.n_components)
    max_id = np.argmax(bc)
    max_covar_id = np.argmax(model.covars_)
    ids = np.argwhere(model._covars_.flatten() > 100).flatten()

    used = np.argwhere(bc != 0).flatten()
    probs = bc/float(sum(bc))

    mapped = {}
    # model.algorithm = 'map'

    import random
    import sklearn.mixture

    ids = ids[0:len(used)]

    for id in ids:
        # replace_id = np.random.choice(used)
        # randomly select node to clone according to its "information weight"
        # replace_id = np.random.choice(model.n_components,p=probs)
        replace_id = random.choices(range(model.n_components),weights=bc)[0]

        mapped[id] = [replace_id, 2*bc[replace_id], int(model.transmat_[replace_id,replace_id]*1000)/1000]


        # lower prob of used node
        # allow cloning of both
        bc[replace_id] //= 2
        bc[id] = bc[replace_id]

        size = model.n_components
        ord = np.random.binomial(1,0.5,model.n_components)
        nord = 1 - ord

        mapped[id].append('g')
        in_trans = model.transmat_[:,id].copy()
        # clone the not used node
        # out transitions (row) like in original
        model.transmat_[id,ord] = model.transmat_[replace_id,ord]
        model.transmat_[id,nord] = 2e-290
        model.transmat_[replace_id,ord] =  2e-290

        # in trasitions (column) half for each of two (original and clone)
        model.transmat_[:,replace_id] /= 2.
        model.transmat_[:,id] = in_trans/2. + model.transmat_[:,replace_id]
        # model.transmat_[:,replace_id] += in_trans/2.

        # original trans should be small, add to them to keep row normalization to 1
        utils.normalize(model.transmat_, 1)

        model.startprob_[replace_id] /= 2.
        model.startprob_[id] += model.startprob_[replace_id]

        # try:
        #     gmm = sklearn.mixture.GMM(n_components=2, verbose=False)
        #     gmm.fit(signal[pred == replace_id])
        #     model.means_[id] = gmm.means_[0]
        #     model.means_[replace_id] = gmm.means_[1]
        #     model._covars_[id] = gmm.covars_[0]
        #     model._covars_[replace_id] = gmm.covars_[1]
        # except:
        model.means_[id] = model.means_[replace_id]
        # diverge them slighly to cover more ground
        # model.means_[replace_id] *= 1.001
        model._covars_[id] = model._covars_[replace_id]


    print("fixed no nodes",len(ids), mapped)

def fix_unused_best(model, signal):
    pred = model.predict(signal)
    bc = np.bincount(pred,minlength=model.n_components)
    max_id = np.argmax(bc)
    max_covar_id = np.argmax(model.covars_)
    ids = np.argwhere(bc == 0).flatten()
    used = np.argwhere(bc != 0).flatten()
    probs = bc/float(sum(bc))

    mapped = {}
    # model.algorithm = 'map'

    import random
    import sklearn.mixture

    ids = ids[0:len(used)]

    for id in ids:
        # replace_id = np.random.choice(used)
        # randomly select node to clone according to its "information weight"
        # replace_id = np.random.choice(model.n_components,p=probs)
        replace_id = random.choices(range(model.n_components),weights=bc)[0]

        mapped[id] = [replace_id, 2*bc[replace_id], int(model.transmat_[replace_id,replace_id]*1000)/1000]



        # if (np.sum(model.transmat_[:,replace_id])) > 3):
        # unroll thight self loop
        if model.transmat_[replace_id,replace_id] > 0.1:
            # can clone this state any more
            bc[replace_id] = 0
            bc[id] = bc[replace_id]

            mapped[id].append('s')
            in_trans = model.transmat_[:,id].copy()
            model.transmat_[id,:] = model.transmat_[replace_id,:]
            model.transmat_[replace_id,id] += model.transmat_[replace_id,replace_id]
            model.transmat_[id,id] += model.transmat_[replace_id,replace_id]
            model.transmat_[replace_id,replace_id] = 2e-290

            # staing in giver state is forbidden
            # in place of that transit to cloned state
            # model.transmat_[replace_id,id] += model.transmat_[replace_id,replace_id]
            # model.transmat_[replace_id,replace_id] = 0.0001
            utils.normalize(model.transmat_, 1)

            model.startprob_[replace_id] /= 2.
            model.startprob_[id] += model.startprob_[replace_id]

            model.means_[id] = model.means_[replace_id]
            # diverge them slighly to cover more ground
            # model.means_[replace_id] *= 1.001
            model._covars_[id] = model._covars_[replace_id]
        #TODO: unroll longer loops

        #refit to general node
        # to many ins, to many out, to large emission - coverage
        else:
            # lower prob of used node
            # allow cloning of both
            bc[replace_id] //= 2
            bc[id] = bc[replace_id]

            size = model.n_components
            ord = np.random.binomial(1,0.5,model.n_components)
            nord = 1 - ord

            mapped[id].append('g')
            in_trans = model.transmat_[:,id].copy()
            # clone the not used node
            # out transitions (row) like in original
            model.transmat_[id,ord] = model.transmat_[replace_id,ord]
            model.transmat_[id,nord] = 2e-290
            model.transmat_[replace_id,ord] =  2e-290

            # in trasitions (column) half for each of two (original and clone)
            model.transmat_[:,replace_id] /= 2.
            model.transmat_[:,id] = in_trans/2. + model.transmat_[:,replace_id]
            # model.transmat_[:,replace_id] += in_trans/2.

            # original trans should be small, add to them to keep row normalization to 1
            utils.normalize(model.transmat_, 1)

            model.startprob_[replace_id] /= 2.
            model.startprob_[id] += model.startprob_[replace_id]

            # try:
            #     gmm = sklearn.mixture.GMM(n_components=2, verbose=False)
            #     gmm.fit(signal[pred == replace_id])
            #     model.means_[id] = gmm.means_[0]
            #     model.means_[replace_id] = gmm.means_[1]
            #     model._covars_[id] = gmm.covars_[0]
            #     model._covars_[replace_id] = gmm.covars_[1]
            # except:
            model.means_[id] = model.means_[replace_id]
            # diverge them slighly to cover more ground
            # model.means_[replace_id] *= 1.001
            model._covars_[id] = model._covars_[replace_id]


    print("fixed no nodes",len(ids), mapped)

def fix_unused_unroll(model, signal):
    pred = model.predict(signal)
    bc = np.bincount(pred,minlength=model.n_components)
    max_id = np.argmax(bc)
    max_covar_id = np.argmax(model.covars_)
    ids = np.argwhere(bc == 0).flatten()
    used = np.argwhere(bc != 0).flatten()
    probs = bc/float(sum(bc))

    mapped = {}

    import random
    import sklearn.mixture

    ids = ids[0:len(used)]

    for id in ids:
        # replace_id = np.random.choice(used)
        # randomly select node to clone according to its "information weight"
        # replace_id = np.random.choice(model.n_components,p=probs)
        replace_id = random.choices(range(model.n_components),weights=bc)[0]

        mapped[id] = (replace_id, 2*bc[replace_id])

        # lower prob of used node
        bc[replace_id] = 0
        # this will make:
        # cloned states for clone fail in GMixture, and make a identical copy
        # cloned states from origin to have same GMixture, and idendical copy as well
        # TODO: if thats okay - store relation and avoid refitting GMixture
        bc[id] = bc[replace_id]


        in_trans = model.transmat_[:,id].copy()

        model.transmat_[id,:] = model.transmat_[replace_id,:]
        model.transmat_[replace_id,id] += model.transmat_[replace_id,replace_id]
        model.transmat_[id,id] += model.transmat_[replace_id,replace_id]
        model.transmat_[replace_id,replace_id] = 2e-290

        # staing in giver state is forbidden
        # in place of that transit to cloned state
        # model.transmat_[replace_id,id] += model.transmat_[replace_id,replace_id]
        # model.transmat_[replace_id,replace_id] = 0.0001
        utils.normalize(model.transmat_, 1)

        model.startprob_[replace_id] /= 2.
        model.startprob_[id] += model.startprob_[replace_id]

        model.means_[id] = model.means_[replace_id]
        # diverge them slighly to cover more ground
        # model.means_[replace_id] *= 1.001
        model._covars_[id] = model._covars_[replace_id]


    print("fixed no nodes",len(ids), mapped)

def fix_unused_fair(model, signal):
    pred = model.predict(signal)
    bc = np.bincount(pred,minlength=model.n_components)
    max_id = np.argmax(bc)
    max_covar_id = np.argmax(model.covars_)
    ids = np.argwhere(bc == 0).flatten()
    used = np.argwhere(bc != 0).flatten()
    probs = bc/float(sum(bc))

    mapped = {}

    import random
    import sklearn.mixture

    for id in ids:
        # replace_id = np.random.choice(used)
        # randomly select node to clone according to its "information weight"
        # replace_id = np.random.choice(model.n_components,p=probs)
        replace_id = random.choices(range(model.n_components),weights=bc)[0]
        # lower prob of used node
        bc[replace_id] //= 2
        # this will make:
        # cloned states for clone fail in GMixture, and make a identical copy
        # cloned states from origin to have same GMixture, and idendical copy as well
        # TODO: if thats okay - store relation and avoid refitting GMixture
        bc[id] = bc[replace_id]

        mapped[id] = (replace_id, 2*bc[replace_id])

        in_trans = model.transmat_[:,id].copy()
        # clone the not used node
        # out transitions (row) like in original
        model.transmat_[id,:] = model.transmat_[replace_id,:]
        # model.transmat_[id,replace_id] = node_trans
        # model.means_[replace_id] *= 0.99
        # in trasitions (column) half for each of two (original and clone)
        model.transmat_[:,replace_id] /= 2.
        # original trans should be small, add to them to keep row normalization to 1
        model.transmat_[:,id] = in_trans + model.transmat_[:,replace_id]
        # staing in giver state is forbidden
        # in place of that transit to cloned state
        # model.transmat_[replace_id,id] += model.transmat_[replace_id,replace_id]
        # model.transmat_[replace_id,replace_id] = 0.0001
        utils.normalize(model.transmat_, 1)
        model.startprob_[replace_id] /= 2.
        model.startprob_[id] += model.startprob_[replace_id]

        try:
            gmm = sklearn.mixture.GMM(n_components=2, verbose=False)
            gmm.fit(signal[pred == replace_id])
            model.means_[id] = gmm.means_[0]
            model.means_[replace_id] = gmm.means_[1]
            model._covars_[id] = gmm.covars_[0]
            model._covars_[replace_id] = gmm.covars_[1]
        except:
            model.means_[id] = model.means_[replace_id]
            # diverge them slighly to cover more ground
            # model.means_[replace_id] *= 1.001
            model._covars_[id] = model._covars_[replace_id]


    print("fixed no nodes",len(ids), mapped)
