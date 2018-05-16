import sys as _sys
from keyword import iskeyword as _iskeyword
from .memoryslots import memoryslots
import re

def isidentifier(s):
    return re.match(r'^[a-z_][a-z0-9_]*$', s, re.I) is not None

_class_template = """\
from collections import OrderedDict
from recordclass.memoryslots import memoryslots, itemgetset

_property = property
_tuple = tuple
_memoryslots = memoryslots
_itemgetset = itemgetset

class {typename}(memoryslots):
    '{typename}({arg_list})'

    __slots__ = ()

    _fields = tuple({field_names!r})

    def __new__(_cls, {arg_list}):
        'Create new instance of {typename}({arg_list})'
        return _memoryslots.__new__(_cls, {arg_list})

    @classmethod
    def _make(_cls, iterable):
        'Make a new {typename} object from a sequence or iterable'
        result = _memoryslots.__new__(_cls, *iterable)
        if len(result) != {num_fields:d}:
            raise TypeError('Expected {num_fields:d} arguments, got %d' % len(result))
        return result

    def _replace(_self, **kwds):
        'Return a new {typename} object replacing specified fields with new values'
        for name, val in kwds.items():
            setattr(_self, name, val)
        return _self

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '({repr_fmt})' % tuple(self)

    def _asdict(self):
        'Return a new OrderedDict which maps field names to their values'
        return OrderedDict(zip(self.__class__._fields, self ))

    __dict__ = _property(_asdict)
        
    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return tuple(self)

    def __getstate__(self):
        'Exclude the OrderedDict from pickling'
        return None
        
    def __reduce__(self):
        'Reduce'
        return type(self), tuple(self)

{field_defs}
"""

_repr_template = '{name}=%r'

_field_template = '    {name} = _itemgetset({index:d})'

# _field_template = '''\
#     def __{name}_get(self):
#         return self[{index:d}]
#     def __{name}_set(self, val):
#         self[{index:d}] = val
#     {name} = _property(__{name}_get, __{name}_set, doc='Alias for field number {index:d}')
#     del __{name}_set, __{name}_get'''

def recordclass(typename, field_names, verbose=False, rename=False, source=True):
    """Returns a new subclass of array with named fields.

    >>> Point = recordarray('Point', ['x', 'y'])
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
    >>> x, y = p                        # unpack like a regular tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessable by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)
    """

    # Validate the field names.  At the user's option, either generate an error
    # message or automatically replace the field name with a valid name.
    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    field_names = list(map(str, field_names))
    typename = str(typename)
    if rename:
        seen = set()
        for index, name in enumerate(field_names):
            if (not isidentifier(name)
                or _iskeyword(name)
                or name.startswith('_')
                or name in seen):
                field_names[index] = '_%d' % index
            seen.add(name)
    for name in [typename] + field_names:
        if type(name) != str:
            raise TypeError('Type names and field names must be strings')
        if not isidentifier(name):
            raise ValueError('Type names and field names must be valid '
                             'identifiers: %r' % name)
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a '
                             'keyword: %r' % name)
    seen = set()
    for name in field_names:
        if name.startswith('_') and not rename:
            raise ValueError('Field names cannot start with an underscore: '
                             '%r' % name)
        if name in seen:
            raise ValueError('Encountered duplicate field name: %r' % name)
        seen.add(name)

    # Fill-in the class template
    class_definition = _class_template.format(
        typename = typename,
        field_names = tuple(field_names),
        num_fields = len(field_names),
        arg_list = repr(tuple(field_names)).replace("'", "")[1:-1],
        repr_fmt = ', '.join(_repr_template.format(name=name)
                             for name in field_names),
        field_defs = '\n'.join(_field_template.format(index=index, name=name)
                               for index, name in enumerate(field_names))
    )

    # Execute the template string in a temporary namespace and support
    # tracing utilities by setting a value for frame.f_globals['__name__']
    namespace = dict(__name__='recorclass_' + typename)
    code = compile(class_definition, "", "exec")
    eval(code, namespace)
    result = namespace[typename]
    if source:
        result._source = class_definition
    if verbose:
        print(result._source)

    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in environments where
    # sys._getframe is not defined (Jython for example) or sys._getframe is not
    # defined for arguments greater than 0 (IronPython).
    try:
        result.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass

    return result

