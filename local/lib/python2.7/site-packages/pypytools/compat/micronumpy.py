"""
numpy/numpypy compatibility layer
---------------------------------

Nowadays, the recommended way to install numpy on PyPy is to simply run::

  pip install numpy

It installs the "original" numpy package through cpyext, PyPy's C-API
compatibility layer. This ensures maximum compatibility, but the drawback is
that cpyext is very slow.

PyPy comes also with its own reimplementation of (very) few numpy
functionalities, internally known as `micronumpy`, and accessible through the
builtin `_numpypy` module. Since it is written in RPython it is very well
integrated with the JIT, and it's super fast.

For example, consider the followin trivial benchmark::

    import time
    import numpy as np
    #from pypytools.compat import micronumpy as np

    def main():
        N = 1000000
        a = np.zeros(N)
        t1 = time.time()
        tot = 0
        for item in a:
            tot += item
        t2 = time.time()
        print '%d ms' % ((t2-t1)*1000)

On my machine, I get the following results:

  - CPython:          251 ms
  - PyPy + numpy:    2962 ms
  - PyPy + micronumpy: 36 ms

**WARNING**: as written above, micronumpy might not be 100% compatible with
numpy: you should make sure to test your program both on PyPy and CPython, and
check that you get the same results.

The goal of this module is to make it easier to use micronumpy, if you need
the extra performance; in particular:

  - on PyPy, it rearranges _numpypy in a way which makes it a subset of numpy,
    so that in simple cases you can simply use the pattern `from
    pypytools.compat import micronumpy as np`

  - on CPython, it falls back to numpy. This means that you can simply import
    `pypytools.compat.micronumpy` even on CPython, and it should "just work"
"""

import pypytools
if pypytools.IS_PYPY:
    IS_MICRONUMPY = True
    from _numpypy.multiarray import *
    from _numpypy.umath import *

    def asarray(a, dtype=None, order=None):
        return array(a, dtype, copy=False, order=order)

    def array_equal(a1, a2):
        try:
            a1, a2 = asarray(a1), asarray(a2)
        except:
            return False
        if a1.shape != a2.shape:
            return False
        return bool(asarray(a1 == a2).all())

    PZERO = float('0.0')
    NZERO = float('-0.0')
    PINF = float('inf')
    NINF = float('-inf')
    NAN = float('nan')
    euler_gamma = 0.577215664901532860606512090082402431 # from npy_math.h
    Inf = inf = infty = Infinity = PINF
    nan = NaN = NAN
    from math import e, pi

    # generate wrappers for ndarray's methods
    def make_wrappers():
        from pypytools.codegen import Code
        code = Code()
        names = ['all', 'any', 'argmax', 'argmin', 'argsort', 'choose', 'clip',
                 'copy', 'cumprod', 'cumsum', 'diagonal', 'max', 'min',
                 'nonzero', 'prod', 'ptp', 'put', 'ravel', 'repeat', 'reshape',
                 'round', 'squeeze', 'sum', 'swapaxes', 'transpose']
        #
        for name in names:
            ns = code.new_scope(name=name)
            with code.def_(name, ['myarray'], '*args', '**kwargs'):
                ns.w('return myarray.{name}(*args, **kwargs)')
        #
        code.compile()
        gbl = globals()
        for name in names:
            gbl[name] = code[name]

    make_wrappers()
    del make_wrappers

else:
    IS_MICRONUMPY = False
    from numpy import *
    from numpy.core import round, max, min
