import wfdb
import hmm
import numpy as np
import matplotlib.pyplot as plt


print "Preprocessing"
sig, fields = wfdb.rdsamp('100')

ecg = sig[:10000,0]
diff = np.diff(ecg)

dmax = np.max(diff)
dmin = np.min(diff)
count = 100
bins = [ dmin + (dmax - dmin)/count * i for i in xrange(count+1) ]
quantized = np.digitize(diff, bins)

dequant = np.empty(len(quantized))

for i in xrange(len(dequant)):
    v = quantized[i]
    v = min(v, count-1)
    dequant[i] = bins[v]


print "Model training"
states = 10
model = hmm.random_model(states, count+2)

model = hmm.baum_welch(quantized, model)


print "Questions answering"
hmm.probabilities(model, 5)
