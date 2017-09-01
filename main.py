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

    line = ((0,0), (xoffset,yoffset))
    lines.append(line)

    xoffset += 2*xincrement
    xleft += xincrement
    xright += xincrement

    reduce_lst = []

    class Node():
        def __init__(self, depth, left=None, right=None):
            self.depth = depth
            self.left = left
            self.right = right

        def isleaf(self):
            return (self.left is None and self.right is None)

    stack = []
    buf = [Node(1) for _ in range(N_tokens)]
    lines = []

    for i, t in enumerate(transitions):
        if t == SHIFT:
            stack.append(buf.pop())
        if t == REDUCE:
            right = stack.pop()
            left = stack.pop()
            new_stack_item = Node(max(left.depth, right.depth) + 1, left, right)
            stack.append(new_stack_item)

    def _draw_left(root, draw_left):
        # If left is leaf, return False.
        # If draw_left is True, then draw line from
        # root to leaf.
        lines.append(None)
        return root.left.isleaf()

    def _draw_right(root, draw_right):
        # If right is leaf, return False.
        # If draw_left is True, then draw line from
        # root to leaf.
        lines.append(None)
        return root.right.isleaf()

    def draw(root, draw_left, draw_right):

        continue_left = _draw_left(root, draw_left)
        continue_right = _draw_right(root, draw_right)

        if continue_left:
            # The line from the root to furthest left leaf
            # has already been drawn!
            draw(root[0], False, True)

        if continue_right:
            # The line from the root to furthest right leaf
            # has already been drawn!
            draw(root[1], True, False)

    draw(stack, True, True)

    return lines


if __name__ == '__main__':

    gflags.DEFINE_string("input", "x,l,r,r,x", "input")
    gflags.DEFINE_float("width", 6.0, "width")
    gflags.DEFINE_float("height", -1.0, "height")
    gflags.DEFINE_integer("precision", 2, "precision")
    gflags.DEFINE_enum("style", "simple", ["simple", "shift-reduce"], "style")

    FLAGS(sys.argv)
    print("Flags: " + json.dumps(FLAGS.flag_values_dict(), sort_keys=True, indent=4))

    if FLAGS.style == "simple":
        lines = latex_trees(FLAGS.input.split(','), FLAGS.width, FLAGS.height, FLAGS.precision)
    elif FLAGS.style == "shift-reduce":
        lines = latex_trees_sr(list(map(int, FLAGS.input)), FLAGS.width, FLAGS.height, FLAGS.precision)

    print(lines)
    for line in lines:
        print("\draw [line width=0.25mm] {} -- {};".format(line[0], line[1]))
