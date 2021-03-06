from functools import reduce
import operator as op
import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_raises, assert_allclose
from scipy import linalg

from mcmodels.utils \
    import (nonzero_unique, unionize, ordered_unique, lex_ordered_unique,
            padded_diagonal_fill, squared_norm)


# ============================================================================
# Module level functions
# ============================================================================
def test_nonzero_unique():
    # ------------------------------------------------------------------------
    # test unique without zero
    a = [0, 5, 1, 2, 0, 4, 0, 5]
    nonzero_unq = [1, 2, 4, 5]

    assert_allclose(nonzero_unq, nonzero_unique(a))


def test_ordered_unique():
    # ------------------------------------------------------------------------
    # test standard output
    arr = [0, 1, 1, 2, 5, 7, 1, 5, 2, 9, 6, 2, 6]
    unq = [0, 1, 2, 5, 7, 9, 6]
    idx = list(map(arr.index, unq))
    cnt = list(map(arr.count, unq))

    unique = ordered_unique(arr)
    assert_array_equal(unique, unq)

    # ------------------------------------------------------------------------
    # test return index
    unique, index = ordered_unique(arr, return_index=True)
    assert_array_equal(unique, unq)
    assert_array_equal(index, idx)

    # ------------------------------------------------------------------------
    # test return counts
    unique, counts = ordered_unique(arr, return_counts=True)
    assert_array_equal(unique, unq)
    assert_array_equal(counts, cnt)

    # ------------------------------------------------------------------------
    # test return counts & index
    unique, index, counts = ordered_unique(arr, return_index=True,
                                           return_counts=True)
    assert_array_equal(unique, unq)
    assert_array_equal(index, idx)
    assert_array_equal(counts, cnt)


def test_lex_ordered_unique():
    # ------------------------------------------------------------------------
    # test standard output
    arr = [0, 1, 1, 2, 5, 7, 1, 5, 2, 9, 6, 2, 6]
    unq = [1, 5, 7, 6, 0, 9, 2]
    idx = list(map(arr.index, unq))
    cnt = list(map(arr.count, unq))

    unique = lex_ordered_unique(arr, unq)
    assert_array_equal(unique, unq)

    # ------------------------------------------------------------------------
    # test return index
    unique, index = lex_ordered_unique(arr, unq, return_index=True)
    assert_array_equal(unique, unq)
    assert_array_equal(index, idx)

    # ------------------------------------------------------------------------
    # test return counts
    unique, counts = lex_ordered_unique(arr, unq, return_counts=True)
    assert_array_equal(unique, unq)
    assert_array_equal(counts, cnt)

    # ------------------------------------------------------------------------
    # test return counts & index
    unique, index, counts = lex_ordered_unique(arr, unq, return_index=True,
                                               return_counts=True)
    assert_array_equal(unique, unq)
    assert_array_equal(index, idx)
    assert_array_equal(counts, cnt)

    # ------------------------------------------------------------------------
    # test extra value in lex order (not in arr)
    extra = lex_ordered_unique(arr, unq+[10], allow_extra=True)
    assert_array_equal(extra, unq)

    # ------------------------------------------------------------------------
    # test duplicate raises error
    assert_raises(ValueError, lex_ordered_unique, arr, unq+[0])

    # ------------------------------------------------------------------------
    # test lex order has not changed
    assert isinstance(unq, list)


def test_padded_diagonal_fill():
    # ------------------------------------------------------------------------
    # test shape and sum match (extra filled with 0.)
    a = 1 * np.ones((2, 5))
    b = 2 * np.ones((1, 4))
    c = 3 * np.ones((3, 1))
    d = 4 * np.ones((1, 1))
    arrs = (a, b, c, d)

    filled = padded_diagonal_fill(arrs)

    assert filled.shape == (7, 11)
    assert filled.sum() == reduce(op.add, map(np.sum, arrs))

    # ------------------------------------------------------------------------
    # test return is consistent
    assert_array_equal(filled[0:2, 0:5], a)
    assert_array_equal(filled[2:3, 5:9], b)
    assert_array_equal(filled[3:6, 9:10], c)
    assert_array_equal(filled[6:7, 10:11], d)


def test_squared_norm():
    # ------------------------------------------------------------------------
    # test consistent with scipy.linalg.norm
    a = np.random.rand(10000)
    b = np.random.rand(100, 100)

    assert_allclose(squared_norm(a), linalg.norm(a)**2)
    assert_allclose(squared_norm(b), linalg.norm(b)**2)


def test_unionize():
    # ------------------------------------------------------------------------
    # test output correct
    volume = np.ones((10, 10))
    key = np.hstack((np.arange(5), np.arange(5)))
    result = 2 * np.ones((10, 4)) # only nonzero

    assert_array_equal(unionize(volume, key), result)

    # ------------------------------------------------------------------------
    # test incompatible key shape
    key = np.arange(9)

    assert_raises(ValueError, unionize, volume, key)
