#!/usr/bin/env python

def heapsort(ary, strategy = 'up'):
    swaps = 0
    def swap(i,j):
        nonlocal swaps
        swaps += 1
        ary[i], ary[j] = ary[j], ary[i]

    lst = len(ary)

    def siftup(pos):
        while pos:
            if ary[pos] < ary[pos//2]:
                swap(pos,pos//2)
                pos //= 2
            else:
                break
    def siftdown(pos, end):
        while pos < end:
            left = 2*pos if 2*pos < end else pos
            right = 2*pos + 1 if 2 * pos + 1 < end else pos
            toswap = pos
            if ary[pos] > ary[left]:
                toswap = left
            if ary[toswap] > ary[right]:
                toswap = right
            if toswap == pos:
                break
            swap(pos, toswap)
            pos = toswap


    # build heap starting from first element
    # print("before", ary)
    if strategy == 'down':
        for i in range(lst):
            siftup(i)
    else:
        for i in range(lst-1, -1, -1):
            siftdown(i,lst)
    print("swaps", swaps)

    # print("heapyfied", ary)
    for i in range(lst-1, 0, -1):
        swap(0,i)
        siftdown(0,i)

    # print("sorted", ary)
    # sort tree swapping element for end, and rebuilding tree


class BinaryHeap():
    def __init__(self ):
        self._ary = []
    def push(self, item):
        pos = len(self._ary)
        self._ary.append(item)
        self.siftup(pos)
    def siftup(self, pos):
        while pos:
            if self._ary[pos] < self._ary[pos//2]:
                self._ary[pos], self._ary[pos//2] = self._ary[pos//2], self._ary[pos]
                pos //= 2
            else:
                break
    def pop(self):
        lst = len(self._ary)
        item = None
        print(lst, item)
        if lst >= 1:
            self._ary[0], self._ary[lst-1] = self._ary[lst-1],self._ary[0]
            item = self._ary.pop()
            print(lst, item)
            self.siftdown(0)
        return item
    def siftdown(self, pos):
        lst = len(self._ary)
        if lst == 0:
            return None
        while pos < lst:
            left = 2 * pos
            right = 2 * pos + 1
            left = pos if left >= lst else left
            right = pos if right >= lst else right
            swap = pos
            print("siftdown pos {} left {} right {} swap {} of len {}".format(pos, left, right, swap, len(self._ary)))
            # if self._ary[left] >= self._ary[pos] <= self.ary[right]:
            #     return
            if self._ary[pos] > self._ary[left]:
                swap = left
            if self._ary[swap] > self._ary[right]:
                swap = right
            if swap == pos:
                return
            self._ary[pos], self._ary[swap] = self._ary[swap], self._ary[pos]
            pos = swap


if __name__ == '__main__':
    import random
    ary = list(range(1,10000))
    random.shuffle(ary)
    heapsort(ary, 'up')
    srt = []
    # heap = BinaryHeap()
    # for i in ary:
    #     heap.push(i)
    #
    #
    # print("heap", heap._ary)
    # item = heap.pop()
    # while item:
    #     print(item, heap._ary)
    #     srt.append(item)
    #     item = heap.pop()
    #
    #
    # print("sorted", srt)
