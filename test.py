import unittest

from main import latex_trees_sr


def almost_eq(a, b, eps=1e-4):
    return abs(a - b) < eps


def check(expected, actual):

    assert len(expected) == len(actual)

    # for line in lines:
    for i, (exp, act) in enumerate(zip(expected, actual)):

        assert len(exp) == len(act)

        # for i in [start, end]:
        for exp_i, act_i in zip(exp, act):

            assert almost_eq(exp_i[0], act_i[0]) and almost_eq(exp_i[1], act_i[1]),\
                "line {}: exp={} != act={}".format(i, exp, act)


class TestLatexTreesSR(unittest.TestCase):

    def test_lb_5(self):
        transitions = list(map(int, '001010101'))
        width = 6.0
        height = -1.0
        expected = [
            ((0.,0.), (-3,-1)),
            ((-2.25,-0.75), (-1.5,-1)),
            ((-1.5,-0.5), (0,-1)),
            ((-0.75,-0.25), (1.5,-1)),
            ((0.,0.), (3,-1)),
            ]
        actual = latex_trees_sr(transitions, width, height)
        check(expected, actual)

    def test_rb_5(self):
        transitions = list(map(int, '000001111'))
        width = 6.0
        height = -1.0
        expected = [
            ((0.,0.), (-3,-1)),
            ((0.75,-0.25), (-1.5,-1)),
            ((1.5,-0.5), (0,-1)),
            ((2.25,-0.75), (1.5,-1)),
            ((0.,0.), (3,-1)),
            ]
        actual = latex_trees_sr(transitions, width, height)
        check(expected, actual)

    def test_001000111(self):
        transitions = list(map(int, '001000111'))
        width = 6.0
        height = -1.0
        expected = [
            ((0.,0.), (-3,-1)),
            ((-2.25,-0.75), (-1.5,-1)),
            ((1.5,-0.5), (0,-1)),
            ((2.25,-0.75), (1.5,-1)),
            ((0.,0.), (3,-1)),
            ]
        actual = latex_trees_sr(transitions, width, height)
        check(expected, actual)

    def test_0000101010111(self):
        transitions = list(map(int, '0000101010111'))
        width = 6.0
        height = -1.2
        expected = [
            ((0,0), (-3,-1.2)),
            ((0.5,-0.2), (-2,-1.2)),
            ((1,-0.4), (-1,-1.2)),
            ((-0.5,-1), (0,-1.2)),
            ((0,-0.8), (1,-1.2)),
            ((0.5,-0.6), (2,-1.2)),
            ((0,0), (3,-1.2)),
            ]
        actual = latex_trees_sr(transitions, width, height)
        check(expected, actual)

    def test_000110101(self):
        transitions = list(map(int, '000110101'))
        width = 8.0
        height = -1.2
        expected = [
            ((0,0), (-4,-1.2)),
            ((-1,-0.9), (-2,-1.2)),
            ((-2,-0.6), (0,-1.2)),
            ((-1,-0.3), (2,-1.2)),
            ((0,0), (4,-1.2)),
            ]
        actual = latex_trees_sr(transitions, width, height)
        check(expected, actual)


if __name__ == '__main__':
    unittest.main()
