import types
from sys import version_info

PY3 = version_info.major == 3

def clonefunc(f):
    """Deep clone the given function to create a new one.

    By default, the PyPy JIT specializes the assembler based on f.__code__:
    clonefunc makes sure that you will get a new function with a **different**
    __code__, so that PyPy will produce independent assembler. This is useful
    e.g. for benchmarks and microbenchmarks, so you can make sure to compare
    apples to apples.

    Use it with caution: if abused, this might easily produce an explosion of
    produced assembler.
    """
    # first of all, we clone the code object
    co = f.__code__
    args = [co.co_argcount, co.co_nlocals, co.co_stacksize, co.co_flags, co.co_code,
            co.co_consts, co.co_names, co.co_varnames, co.co_filename, co.co_name,
            co.co_firstlineno, co.co_lnotab, co.co_freevars, co.co_cellvars]
    if PY3:
        args.insert(1, co.co_kwonlyargcount)
    co2 = types.CodeType(*args)
    #
    # then, we clone the function itself, using the new co2
    f2 = types.FunctionType(co2, f.__globals__, f.__name__, f.__defaults__, f.__closure__)
    return f2
