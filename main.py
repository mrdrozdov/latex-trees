#!/bin/python3

import sys
import json
import gflags

FLAGS = gflags.FLAGS


EDGE = 'x'
LEFT = 'l'
RIGHT = 'r'

SHIFT = 0
REDUCE = 1


def sign(x):
    return -1 if x < 0 else 1


def latex_trees(tokens, width, height, precision=2):

    N = len(tokens)

    xincrement = width/(N-1)/2
    yincrement = height/(N-1)

    leftx = -width/2
    rightx = 0.0
    lefty = height
    righty = 0.0

    # When left, use leftx + xincrement. Then increment leftx/rightx
    # by xincrement.
    # When right, use rightx + xincrement. Then increment leftx/rightx
    # by xincrement.

    lines = []

    for i, tkn in enumerate(tokens):
        if i == 0:
            assert tkn == EDGE
            start = (0.0, 0.0)
        if i == N - 1:
            assert tkn == EDGE
            start = (0.0, 0.0)
        if tkn == LEFT:
            start = (leftx + xincrement, lefty - i * yincrement)
            leftx += xincrement
            rightx += xincrement
        if tkn == RIGHT:
            start = (rightx + xincrement, righty + i * yincrement)
            leftx += xincrement
            rightx += xincrement
            leftx += xincrement
            lefty += yincrement
        previous = tkn

        end = (-width/2 + 2 * i * xincrement, height)  # always the same

        start = tuple(map(lambda x: round(x, precision), start))
        end   = tuple(map(lambda x: round(x, precision), end))

        line = (start, end)
        lines.append(line)
    return lines


def latex_trees_sr(transitions, width, height, precision=2):

    N_transitions = len(transitions)
    N_tokens = int((N_transitions + 1) / 2)

    xincrement = width/(N_tokens-1)/2
    yincrement = height/(N_tokens-1)

    xoffset = -width/2
    yoffset = height

    xleft = xoffset
    xright = 0
    yleft = yoffset
    yright = 0

    stack = []
    buffer = [()] * N_tokens

    lines = []

    line = ((0,0), (xoffset,yoffset))
    lines.append(line)

    xoffset += 2*xincrement
    xleft += xincrement
    xright += xincrement

    for i, t in enumerate(transitions):
        start, end = None, None
        if t == SHIFT:
            stack.append(())
        if t == REDUCE:
            stack.pop()

            if len(stack) == 1 or i == N_transitions - 1:  # LEFT
                start = (xleft, yleft - yincrement)
                end   = (xoffset, height)
            else:  # RIGHT
                start = (xright, yright + yincrement)
                end   = (xoffset, height)

            xoffset += 2*xincrement
            yleft -= yincrement
            yright += yincrement

            xleft += xincrement
            xright += xincrement

            start = tuple(map(lambda x: round(x, precision), start))
            end   = tuple(map(lambda x: round(x, precision), end))

            line = (start, end)
            lines.append(line)

    return lines


if __name__ == '__main__':

    gflags.DEFINE_string("input", "x,l,r,r,x", "input")
    gflags.DEFINE_float("width", 6.0, "width")
    gflags.DEFINE_float("height", -1.0, "height")
    gflags.DEFINE_integer("precision", 2, "precision")
    gflags.DEFINE_enum("style", "simple", ["simple", "shift-reduce"], "style")

    FLAGS(sys.argv)
    print("Flags: " + json.dumps(FLAGS.flag_values_dict(), sort_keys=True, indent=4))

    if style == "simple":
        lines = latex_trees(FLAGS.input.split(','), FLAGS.width, FLAGS.height, FLAGS.precision)
    else:
        lines = latex_trees_sr(FLAGS.input.split(','), FLAGS.width, FLAGS.height, FLAGS.precision)

    for line in lines:
        print("\draw [line width=0.25mm] {} -- {};".format(line[0], line[1]))
