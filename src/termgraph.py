# Adapted from termgraph by Marcus Kazmierczak
# https://github.com/mkaz/termgraph/blob/master/termgraph.py

import sys

tick = '▇'
sm_tick = '|'

def termgraph(labels, data, width=50):
    # verify data
    print('')
    m = len(labels)
    if m != len(data):
        print(">> Error: Label and data array sizes don't match")
        sys.exit(1)

    total = sum(data)

    # massage data
    ## normalize for graph
    max = 0
    for i in range(m):
        if data[i] > max:
            max = data[i]

    step = max / width
    # display graph
    for i in range(m):
        _print_blocks(labels[i], data[i], step, total)

    print()


def _print_blocks(label, count, step, total):
    #TODO: add flag to hide data labels
    blocks = int(count / step)
    if count < step:
        sys.stdout.write(sm_tick)
    else:
        for i in range(blocks):
            sys.stdout.write(tick)

    print("{:>7.2f}% ".format((count/total)*100), end="")
    print("({})".format(label))