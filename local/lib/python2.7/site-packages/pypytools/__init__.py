import sys
IS_PYPY = hasattr(sys, 'pypy_translation_info')

from pypytools.unroll import unroll
from pypytools.codegen import Code
from pypytools.jitview import JitView
from pypytools.util import clonefunc
from pypytools._fakecython import FakeCython

fakecython = FakeCython()
