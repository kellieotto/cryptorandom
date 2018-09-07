"""Unit tests for cryptorandom sampling functions."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import numpy as np
from ..sample import *


class fake_generator():
    """
    This generator just cycles through the numbers 0,...,9.
    """
    def __init__(self):
        self.counter = 0

    def next(self):
        self.counter += 1
        if self.counter > 9:
            self.counter = self.counter % 10

    def random(self, size=None):
        if size == None:
            self.next()
            return self.counter/10
        else:
            rand = []
            for i in range(size):
                self.next()
                rand.append(self.counter/10)
            return rand

    def randint(self, a, b, size=None):
        """
        Generate random integers between a (inclusive) and b (exclusive).
        size controls the number of ints generated. If size=None, just one is produced.
        """
        assert a <= b, "lower and upper limits are switched"

        if size == None:
            return int(a + (self.random()*10) % (b-a))
        else:
            return np.reshape(np.array([int(a + (self.random()*10) % (b-a)) \
                for i in np.arange(np.prod(size))]), size)
                
                
def test_fake_generator():
    """
    Make sure the fake generator works as expected
    """
    
    ff = fake_generator()
    out = ff.randint(0, 10, 10)
    expected = np.concatenate([np.arange(1, 10), np.zeros(1)])
    assert (out == expected).all()
    assert ff.random() == (expected[-1]+1)/10
    
    ff = fake_generator()
    out = ff.randint(1, 11, 10)
    assert (out == expected+1).all()
    
    ff = fake_generator()
    out = ff.randint(0, 20, 10)
    assert (out == expected).all()
    
    ff = fake_generator()
    out = ff.random(2)
    assert out == [0.1, 0.2]


#def test_random_sample_error():
    # test all the assertion errors
    

def test_fykd():
    """
    Test Fisher-Yates shuffle for random samples, fykd_sample
    """
    ff = fake_generator()
    sam = fykd_sample(5, 2, gen=ff)
    assert sam == [1, 2]
    
    ff = fake_generator()
    sam = randomSample(5, 2, method="Fisher-Yates", prng=ff)
    assert (sam+1 == [1, 2]).all() # shift to 1-index


def test_PIKK():
    """
    Test PIKK
    """
    ff = fake_generator()
    sam = PIKK(5, 2, gen=ff)
    assert (sam == [1, 2]).all()
    
    ff = fake_generator()
    sam = randomSample(5, 2, method="PIKK", prng=ff)
    assert (sam+1 == [1, 2]).all() # shift to 1-index


def test_Cormen():
    """
    Test Cormen et al recursive Random_Sample
    """
    ff = fake_generator()
    sam = Random_Sample(5, 2, gen=ff)
    assert sam == [2, 3]
    
    ff = fake_generator()
    sam = randomSample(5, 2, method="Cormen", prng=ff)
    assert (sam+1 == [2, 3]).all() # shift to 1-index
    

def test_Waterman_R():
    """
    Test Waterman's algorithm R
    """
    ff = fake_generator()
    sam = Algorithm_R(5, 2, gen=ff)
    assert sam == [1, 3]
    
    ff = fake_generator()
    sam = randomSample(5, 2, method="Waterman_R", prng=ff)
    assert (sam+1 == [1, 3]).all() # shift to 1-index


def test_sbi():
    """
    Test sample_by_index
    """
    ff = fake_generator()
    sam = sample_by_index(5, 2, gen=ff)
    assert sam == [2, 3]
    
    ff = fake_generator()
    sam = randomSample(5, 2, method="sample_by_index", prng=ff)
    assert (sam+1 == [2, 3]).all() # shift to 1-index