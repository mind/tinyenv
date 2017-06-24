import os
import sys
import unittest

from tinyenv.flags import flags


class TestFlags(unittest.TestCase):

    # def test_flags(self):
    #     assert not flags()

    def test_flags_env(self):
        argv = sys.argv
        sys.argv = ['mymodel']
        os.environ['TINYFLAGS'] = 'tests/fixtures/flags.json'
        f = flags()
        assert f.iterations == 1000
        assert f.weight_decay == 0
        sys.argv = argv
