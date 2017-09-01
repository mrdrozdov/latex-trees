#!/bin/python3

import sys
import json
import gflags

FLAGS = gflags.FLAGS


SHIFT = 0
REDUCE = 1


def latex_trees_sr(transitions, width, height, precision=2, verbose=False):

    N_transitions = len(transitions)
    N_tokens = int((N_transitions + 1) / 2)

    xincrement = width/(N_tokens-1)/2
    yincrement = height/(N_tokens-1)

    xoffset = -width/2
    xoffset_right = width/2
    yoffset = height

    if verbose:
        print("\n",
              "xoffset", xoffset,"\n",
              "yoffset", yoffset,"\n",
              "xincrement", xincrement, "\n",
              "yincrement", yincrement, "\n",
              ""
              )

    drawn_left = 0

    class Node():
        _isroot = False
        def __init__(self, depth, left=None, right=None):
            self.depth = depth
            self.left = left
            self.right = right

        def isleaf(self):
            return (self.left is None and self.right is None)

    stack = []
    buf = [Node(0) for _ in range(N_tokens)]
    lines = []

    for i, t in enumerate(transitions):
        if t == SHIFT:
            stack.append(buf.pop())
        if t == REDUCE:
            right = stack.pop()
            left = stack.pop()
            new_stack_item = Node(max(left.depth, right.depth) + 1, left, right)
            stack.append(new_stack_item)

    def _increment_left():
        nonlocal drawn_left
        drawn_left = drawn_left + 1

    def _increment_right():
        nonlocal drawn_left
        drawn_left = drawn_left + 1

    def _draw_left(root, draw_left):
        # If draw_left is True, then draw line from
        # root to leaf.
        if draw_left:
            end = (xoffset + drawn_left * 2 * xincrement, yoffset)
            if root._isroot:
                start = (0, 0)
            else:
                start = (end[0] + xincrement * root.depth, yoffset - root.depth * yincrement)
            start = tuple(map(lambda x: round(x, precision), start))
            end   = tuple(map(lambda x: round(x, precision), end))
            line = (start, end)
            lines.append(line)

            if verbose:

                print("\n",
                      "direction", "left",
                      "depth", root.depth, "\n",
                      "xoffset", xoffset,"\n",
                      "yoffset", yoffset,"\n",
                      "xincrement", xincrement, "\n",
                      "yincrement", yincrement, "\n",
                      "line", line, "\n"
                      )

            _increment_left()

    def _draw_right(root, draw_right):
        # If draw_left is True, then draw line from
        # root to leaf.
        if draw_right:
            end = (xoffset + drawn_left * 2 * xincrement, yoffset)
            if root._isroot:
                start = (0, 0)
            else:
                start = (end[0] - xincrement * root.depth, yoffset - root.depth * yincrement)
            start = tuple(map(lambda x: round(x, precision), start))
            end   = tuple(map(lambda x: round(x, precision), end))
            line = (start, end)
            lines.append(line)

            if verbose:
                print("\n",
                      "direction", "right",
                      "depth", root.depth, "\n",
                      "xoffset_right", xoffset_right,"\n",
                      "yoffset", yoffset,"\n",
                      "xincrement", xincrement, "\n",
                      "yincrement", yincrement, "\n",
                      "line", line, "\n"
                      )

            _increment_right()

    def draw(root, draw_left, draw_right):

        _draw_left(root, draw_left)

        if not root.left.isleaf():
            # The line from the root to furthest left leaf
            # has already been drawn!
            draw(root.left, False, True)

        if not root.right.isleaf():
            # The line from the root to furthest right leaf
            # has already been drawn!
            draw(root.right, True, False)

        _draw_right(root, draw_right)

    stack[0]._isroot = True
    draw(stack[0], True, True)

    # Sort by token order.
    lines = sorted(lines, key=lambda x: x[1])

    return lines


if __name__ == '__main__':

    gflags.DEFINE_string("input", "00101", "input")
    gflags.DEFINE_float("width", 6.0, "width")
    gflags.DEFINE_float("height", -1.0, "height")
    gflags.DEFINE_integer("precision", 2, "precision")

    FLAGS(sys.argv)
    print("Flags: " + json.dumps(FLAGS.flag_values_dict(), sort_keys=True, indent=4))

    lines = latex_trees_sr(list(map(int, FLAGS.input)), FLAGS.width, FLAGS.height, FLAGS.precision)

    for line in lines:
        print("\draw [line width=0.25mm] {} -- {};".format(line[0], line[1]))
