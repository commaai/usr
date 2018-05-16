import sys
from pypytools import IS_PYPY

def as_signed(x, bits):
    """
    Interpret the given bits-wide int as if it were signed (2-complement
    repr).

    For examplen, given x=0xFF and bits=8:

    bit pattern = 1111 1111
      - unsigned = 255
      - signed   =  -1

    Since in Python ints are always 64 bits (or 32, depending on sys.maxint),
    we need to extend the sign bit up to the most significant bit.

    In CPython, this is done by using simple math; on PyPy, this is done by
    using raw left/right shift operations, which are faster and better handled
    by the JIT.
    """
    if x >= 1<<(bits-1):
        x -= 1<<bits
    return x

if IS_PYPY:
    import __pypy__

    if sys.maxsize == (1<<63)-1:
        BITSIZE = 64
    else:
        BITSIZE = 32

    def as_signed(x, bits):
        shift = BITSIZE - bits
        x = __pypy__.intop.int_lshift(x, shift) # shift x to the most significant bit
        x = __pypy__.intop.int_rshift(x, shift) # shift it back with sign extension
        return x
