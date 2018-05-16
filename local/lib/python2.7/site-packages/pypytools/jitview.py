from __future__ import print_function
import sys
import dis
import bisect
import linecache
try:
    import pypyjit
except ImportError:
    pass

from pypytools.color import Color
from pypytools.util import PY3

if PY3:
    from io import StringIO
else:
    from cStringIO import StringIO

def disass(obj):
    """
    Very hackish wrapper around dis.dis. Return a dict {addr: human_repr}
    """
    buf = StringIO()
    stdout = sys.stdout
    sys.stdout = buf
    try:
        dis.dis(obj)
    finally:
        sys.stdout = stdout
    #
    res = {}
    lines = buf.getvalue().splitlines()
    for line in lines:
        if len(line) < 10:
            continue
        line = line[10:].strip()
        addr, _ = line.split(' ', 1)
        addr = int(addr)
        res[addr] = line
    return res


class CodePrinter(object):

    def __init__(self):
        self._last = None
        self._indent = 0

    def source(self, filename, lineno):
        line = linecache.getline(filename, lineno)[:-1]
        if line != self._last:
            print(line)
            self._last = line
            self._indent = len(line) - len(line.lstrip())

    def _print(self, s, extra=0):
        indent = ' ' * (self._indent+extra)
        print('%s%s' % (indent, s))

    def bytecode(self, s):
        s = Color.set(Color.lightgray, s)
        self._print(s)

    def llop(self, op):
        s = Color.set(Color.yellow, str(op))
        self._print(s, 4)

class JitView(object):

    _is_hook_installed = False

    def __enter__(self):
        if not JitView._is_hook_installed:
            pypyjit.set_compile_hook(self.on_compile)
            JitView._is_hook_installed = True

    def __exit__(self, etype, evalue, tb):
        pass

    ENTER = __enter__.__code__
    EXIT = __exit__.__code__

    def on_compile(self, info):
        if info.jitdriver_name != 'pypyjit':
            return
        enabled = False
        self.printer = CodePrinter()
        for op in info.operations:
            if op.name == 'debug_merge_point' and op.pycode is self.ENTER:
                enabled = True
            elif op.name == 'debug_merge_point' and op.pycode is self.EXIT:
                enabled = False
            elif op.name == 'label':
                print()
                print(Color.set(Color.green_bg, '-' * 80))
                print()
            elif enabled:
                self._print_op(op)

        pypyjit.set_compile_hook(None)
        JitView._is_hook_installed = False

    def _print_op(self, op):
        if op.name == 'debug_merge_point':
            self._print_debug_merge_point(op)
        else:
            self.printer.llop(op)


    def _find_lineno(self, op):
        linestarts = list(dis.findlinestarts(op.pycode))
        i = bisect.bisect(linestarts, (op.bytecode_no,)) - 1
        if i < 0:
            return -1
        else:
            _, lineno  = linestarts[i]
            return lineno

    def _print_debug_merge_point(self, op):
        bytecodes = disass(op.pycode)
        lineno = self._find_lineno(op)
        opcode = bytecodes.get(op.bytecode_no, '')
        #
        self.printer.source(op.pycode.co_filename, lineno)
        self.printer.bytecode(opcode)


