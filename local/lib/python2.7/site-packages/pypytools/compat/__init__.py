"""
CPython emulation of some of the __pypy__ builtins
"""

from pypytools import IS_PYPY

if IS_PYPY:
    from __pypy__ import newdict
    
else:

    def newdict(type):
        return {}
