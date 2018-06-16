import unittest

import numpy as np

import chainer
from chainer import testing
import chainer.functions as F
import chainer.links as L
import onnx_chainer


@testing.parameterize(
    {'ops': F.elu},
    {'ops': F.hard_sigmoid},
    {'ops': F.leaky_relu},
    {'ops': F.log_softmax},
    {'ops': F.relu},
    {'ops': F.sigmoid},
    {'ops': F.softmax},
    {'ops': F.softplus},
    {'ops': F.tanh},
)
class TestActivations(unittest.TestCase):

    def setUp(self):

        class Model(chainer.Chain):

            def __init__(self, ops):
                super(Model, self).__init__()
                self.ops = ops

            def __call__(self, x):
                return self.ops(x)

        self.model = Model(self.ops)
        self.x = np.random.randn(1, 5).astype(np.float32)

    def test_export_test(self):
        chainer.config.train = False
        onnx_chainer.export(self.model, self.x)

    def test_export_train(self):
        chainer.config.train = True
        onnx_chainer.export(self.model, self.x)


class TestPReLU(unittest.TestCase):

    def setUp(self):

        class Model(chainer.Chain):

            def __init__(self):
                super(Model, self).__init__()
                with self.init_scope():
                    self.prelu = L.PReLU()

            def __call__(self, x):
                return self.prelu(x)

        self.model = Model()
        self.x = np.zeros((1, 5), dtype=np.float32)

    def test_export_test(self):
        chainer.config.train = False
        onnx_chainer.export(self.model, self.x)

    def test_export_train(self):
        chainer.config.train = True
        onnx_chainer.export(self.model, self.x)
