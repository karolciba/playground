import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from hmmlearn import hmm
from hmmlearn import utils

table = pandas.read_csv('euro.csv', delimiter=';')

rate = np.array(table["Kurs"])
change = np.array(table["Zmiana"])
change = np.diff(rate)
# comb = np.column_stack((rate,change))
comb = change.reshape(-1,1)
data = 10*comb[:-100]
test = 10*comb[-100:]

# samples = 2001
# x = 2*np.pi*np.arange(samples)
# rate = 10*np.sin(x/50)
# change = 10*np.cos(x/50)


# rate += np.random.random(samples)
# change += np.random.random(samples)
# data = np.column_stack((rate,change))

# sign = 10*np.sin(x/50)*np.sin(x/40)+10*np.cos(x/30)
# diff = np.diff(sign)[:1000]
# csum = np.cumsum(sign)[:1000]
# sign = sign[:1000]
# data = np.column_stack((sign,csum))
#
# data = sign.reshape(-1,1)


def train(data):
    model = hmm.GaussianHMM(n_components=1*128, tol=1., n_iter=100, verbose = True)
    model.fit(data)
    model.init_params = ''
    return model

def next_prob(model,data):
    _, posteriors = model.score_samples(data)
    x = np.linspace(-15,15,100)
    post = posteriors[-1,:]
    aa = np.column_stack(
            post[i]*mlab.normpdf(x,model.means_[i,1],model._covars_[i,1]**0.5)
            for i in range(0,model.n_components))
    return x,np.sum(aa,axis=1)

def predict(model,data,samples):
    _, posteriors = model.score_samples(data)
    x = np.linspace(-15,15,100)
    post = np.dot(posteriors[-1], model.transmat_)
    xx = np.empty((len(x),samples))
    for j in range(samples):
        aa = np.column_stack(
                post[i]*mlab.normpdf(x,model.means_[i],model._covars_[i]**0.5)
                for i in range(0,model.n_components))
        xx[:,j] = np.sum(aa,axis=1)
        post = np.dot(post, model.transmat_)
    return x,xx

def predict2(model,data,samples,emis=1):
    _, posteriors = model.score_samples(data)
    x = np.linspace(-15,15,100)
    post = np.dot(posteriors[-1], model.transmat_)
    xx = np.empty((len(x),samples))
    for j in range(samples):
        aa = np.column_stack(
                post[i]*mlab.normpdf(x,model.means_[i,emis],model._covars_[i,emis]**0.5)
                for i in range(0,model.n_components))
        xx[:,j] = np.sum(aa,axis=1)
        post = np.dot(post, model.transmat_)
    return x,xx

def states_plot(model,e):
    logprob, posterior = model.score_samples(e)

    plt.clf()
    ax = plt.subplot(211)
    plt.plot(e)
    plt.subplot(212,sharex=ax)
    plt.imshow(posterior.T, aspect='auto')

def plot_usage(model, e):
    logprob, posterior = model.score_samples(e)
    usage = np.sum(posterior.T,axis=1)

    # plt.clf()
    plt.plot(np.sort(usage)/float(sum(usage)))

def plot_map_usage(model, signal):
    # plt.clf()
    model.algorithm = 'map'
    pred = model.predict(signal)
    bc = np.bincount(pred,minlength=model.n_components)
    max_id = np.argmax(bc)
    max_covar_id = np.argmax(model.covars_)
    ids = np.argwhere(bc == 0).flatten()
    used = np.argwhere(bc != 0).flatten()
    probs = bc/float(sum(bc))

    plt.plot(np.sort(probs))

def plot_viterbi_usage(model, signal):
    # plt.clf()
    model.algorithm = 'viterbi'
    pred = model.predict(signal)
    bc = np.bincount(pred,minlength=model.n_components)
    max_id = np.argmax(bc)
    max_covar_id = np.argmax(model.covars_)
    ids = np.argwhere(bc == 0).flatten()
    used = np.argwhere(bc != 0).flatten()
    probs = bc/float(sum(bc))

    plt.plot(np.sort(probs))

def reorder_usage(model, e):
    logprob, posterior = model.score_samples(e)
    usage = np.sum(posterior.T,axis=1)
    keys = np.flip(np.argsort(usage),axis=0)

    model.means_ = model.means_[keys]
    model._covars_ = model._covars_[keys]
    model.startprob_ = model.startprob_[keys]

    model.transmat_ = model.transmat_[keys]
    model.transmat_[:,:] = model.transmat_[:,keys]

def reorder_model(model, e):
    pred = model.predict(e)
    bc = np.bincount(pred,minlength=model.n_components)

    keys = np.flip(np.argsort(bc),axis=0)

    model.means_ = model.means_[keys]
    model._covars_ = model._covars_[keys]
    model.startprob_ = model.startprob_[keys]


    model.transmat_ = model.transmat_[keys]
    model.transmat_[:,:] = model.transmat_[:,keys]

def clone(model):
    from sklearn.externals import joblib
    joblib.dump(model,"/tmp/foobarmodel.pkl")
    return joblib.load("/tmp/foobarmodel.pkl")

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

def fix_unused(model, signal):
    """Unused states decided MAP or viterbi usage"""
    # model.algorithm = 'map'
    # pred = model.predict(signal)
    # usage = np.bincount(pred,minlength=model.n_components)
    # treshold = np.sort(usage)[model.n_components//10]
    #
    # ids = np.argwhere(usage <= treshold).flatten()
    # used = np.argwhere(usage > treshold).flatten()
    # probs = usage/float(sum(usage))

    """Unused states decided on average state probability"""
    logprob, posterior = model.score_samples(signal)
    usage = np.sum(posterior.T,axis=1)
    treshold = np.sort(usage)[model.n_components//10]
    ids = np.argwhere(usage <= treshold).flatten()
    used = np.argwhere(usage > treshold).flatten()
    probs = usage/float(sum(usage))
    ids = np.argwhere(probs <= 0.001).flatten()
    used = np.argwhere(usage > 0.001).flatten()

    mapped = {}
    # model.algorithm = 'map'

    import random
    import sklearn.mixture

    ids = ids[0:len(used)]
    # ids = ids[0:model.n_components//10]

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
            probs[replace_id] //= 2
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
            probs[replace_id] //= 2
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

    print("fixed {} nodes of used {} and unused {}, with map {}".format(len(ids), len(used), model.n_components - len(used), mapped))
