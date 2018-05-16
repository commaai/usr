from __future__ import print_function
import py
import types
import ast

def d(node):
    import astpp
    import codegen
    print(astpp.dump(node))
    print()
    print(codegen.to_source(node))


class Closure(object):

    def __init__(self, fn, **extravars):
        self.fn = fn
        self.extravars = extravars
        #
        if fn.__closure__:
            for freevar, cell in zip(fn.__code__.co_freevars, fn.__closure__):
                if freevar not in self.extravars:
                    self.extravars[freevar] = cell.cell_contents
        #
        makesrc = self._create_src()
        self.tree = ast.parse(makesrc)
        ast.increment_lineno(self.tree, fn.__code__.co_firstlineno-2)

    def _create_src(self):
        freevars = self.extravars.keys()
        innersrc = py.code.Source(self.fn)
        lines = [
            'def make(%s):' % ', '.join(freevars),
            str(innersrc.indent()),
            '    return %s' % self.fn.__name__
            ]
        return '\n'.join(lines)

    def make(self):
        tree = ast.fix_missing_locations(self.tree)
        co = compile(tree, self.fn.__code__.co_filename, 'exec')
        myglobals = self.fn.__globals__
        mylocals = {}
        exec(co, myglobals, mylocals)
        make = mylocals['make']
        return make(**self.extravars)


def fake_unroll(**kwargs):
    def identity(fn):
        return fn
    return identity


class unroll(object):

    def __init__(self, **extravars):
        self.extravars = tupleify(extravars)
        # we need to specify a fake unroll, to ignore the existing @unroll
        # decorator in the fn source code
        self.extravars['unroll'] = fake_unroll

    def __call__(self, fn):
        closure = Closure(fn, **self.extravars)
        unroller = Unroller(self.extravars)
        closure.tree = unroller.visit(closure.tree)
        return closure.make()


class Unroller(ast.NodeTransformer):
    def __init__(self, extravars):
        self.extravars = extravars

    def visit_For(self, node):
        if isinstance(node.iter, ast.Name) and node.iter.id in self.extravars:
            return self.unroll(node)
        return node

    def unroll(self, fornode):
        assert fornode.orelse == []
        items = self.extravars[fornode.iter.id]
        body = []
        for i in range(len(items)):
            item = ast.Subscript(value=ast.Name(id=fornode.iter.id, ctx=ast.Load()),
                                 slice=ast.Index(value=ast.Num(n=i)),
                                 ctx=ast.Load())
            assign = ast.Assign(targets=[fornode.target],
                                value=item)
            body.append(assign)
            body.extend(fornode.body)
        return body


def tupleify(d):
    """
    Convert to tuple all the iterables in d
    """
    for key, value in d.items():
        try:
            iter(value)
        except TypeError:
            pass
        else:
            d[key] = tuple(value)
    return d
