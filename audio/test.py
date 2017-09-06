#!/usr/bin/env python

from pyaudio import PyAudio, paFloat32, paContinue, paComplete
import numpy as np
import time
import matplotlib.pyplot as plt

pa = PyAudio()


def callback(in_data, frame_count, time_info, flag):
    # print len(in_data), frame_count, time_info, flag

    # new_data = [ x**2 for x in in_data ]
    data = np.frombuffer(in_data, dtype=np.float32)
    new = np.copy(data)
    # new *= 4
    # new[1::2] *= 8
    # new[::2] *= 8
    # change left right
    # new[::2], new[1::2] = new[1::2], new[::2]

    callback.data = new
    # import pdb; pdb.set_trace()

    if (callback.counter > 1000):
        return in_data, paComplete
    callback.counter += 1

    return new, paContinue

callback.counter = 0
callback.data = None

stream = pa.open(format = paFloat32,
                 channels = 2,
                 rate = 44100,
                 output = True,
                 input = True,
                 frames_per_buffer = 1024,
                 stream_callback = callback)

while stream.is_active():
    if callback.data is not None:
        left = callback.data[::2]
        right = callback.data[1::2]
        fft_left = np.fft.fft(left)
        fft_right = np.fft.fft(right)

        fft = np.append(fft_left, fft_right)
        # fft = fft_left - fft_right

        plt.clf()
        # plt.plot(callback.data)
        plt.plot(abs(fft))
        plt.ylim(ymax = 1, ymin = 0)
        plt.show(block=False)
    plt.pause(0.01)
    # time.sleep(0.1)

# plt.show()
stream.close()
pa.terminate()
