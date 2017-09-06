#!/usr/bin/env python


# node = [ name, left, right ]
#                7
#       4               10
#  2         5         9
# 1 3         6      8


t1 = [ '1', None, None ]
t3 = [ '3', None, None ]
t2 = [ '2', t1, t3 ]
t6 = [ '6', None, None ]
t5 = [ '5', None, t6 ]
t4 = [ '4', t2, t5 ]
t8 =[ '8', None, None ]
t9 = [ '9', t8, None ]
t10 = [ '10', t9, None ]
t7 = [ '7', t4, t10 ]

head = t7

name = 0
left = 1
right = 2

def descent_right(head):
    current = head[left]
    while current[right] and current[right] != head:
        current = current[right]

    return current

def morris(head):
    current = head
    while current:
        print("Current: ", current[name])
        if not current[left]:
            print("Visiting: ", current[name])
            current = current[right]
            continue
        else:
            nxt = descent_right(current)
            print("Found nxt: ", nxt[name])
            if not nxt[right]:
                print("Threading", nxt[name], "with", current[name])
                nxt[right] = current
                current = current[left]
            else:
                print("Unthreadind", nxt[name], "with", nxt[right][name])
                nxt[right] = None
                print("Visiting- ", current[name])
                current = current[right]

if __name__ == '__main__':
    morris(head)

