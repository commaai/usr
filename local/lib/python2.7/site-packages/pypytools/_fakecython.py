"""
Enable the usage of @cython decorators in pure-python code, WITHOUT the
need of having Cython installed.

Cython is a heavy dependency and it does not make sense to install it on PyPy
*only* for 'import cython' to work.

It seems that the only way to convince cython to evaluate the ``@cython.*``
decorators is to have a textual 'import cython' in the source code. So, the
only way to fake a cython module is to patch sys.modules: we use a context
manager to ensure that sys.modules is patched for as little time as needed.

Example usage::

    from pypytools import fakecython
    with fakecython:
        import cython

    @cython.cfunc
    @cython.locals(a=long, b=long)
    @cython.returns(long)
    def foo(a, b):
        return a+b

"""

import sys

def identity(fn):
    return fn


class FakeCython(object):

    __old_cython = None

    def __enter__(self):
        import sys
        self.__old_cython = sys.modules.pop('cython', None)
        sys.modules['cython'] = self

    def __exit__(self, etype, evalue, tb):
        import sys
        if self.__old_cython is None:
            del sys.modules['cython']
        else:
            sys.modules['cython'] = self.__old_cython
            self.__old_cython = None

    compiled = False

    ccall = staticmethod(identity)
    cfunc = staticmethod(identity)

    @staticmethod
    def returns(t):
        return identity

    # at the moment of writing, @cython.except_ is not a feature of standard
    # Cython, but you need my fork to use it:
    # https://github.com/antocuni/cython/tree/pure-except
    @staticmethod
    def except_(ret):
        return identity

    @staticmethod
    def locals(**kwds):
        return identity

    @staticmethod
    def declare(**kwds):
        pass

