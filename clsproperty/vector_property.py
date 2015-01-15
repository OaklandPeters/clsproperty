"""

Makes getter/setter

Questionable behavior for VectorProperty setter:
    Treat value as seperate assignments to each case?
        map(lambda case: self._set_(case, value), obj)
            
    Or assign whole value to each case?
        map(lambda case, val: self._set_(case, val), obj, value)


@todo: Make this take an optional argument to determine the __iter__ used.
    (Defaults to ~iter(obj), but other desires might be: ~iter(obj.data), etc)
    Set this via method on class: _iter/fitr
@todo: Docstrings
@todo: Unittests

@todo: Advanced version that returns a callable sequence - @VectorMethod
"""
from __future__ import absolute_import
import inspect
import collections
import copy


class VectorProperty(object):
    """
    
    @TODO: Add input checking - self must be sequence (~cases)
    """
    def __init__(self, *fargs, **fkwargs):
        """Check if used as a decorator for a class, or if used conventionally."""          
        (self.fget,
         self.fset,
         self.fdel,
         self.fval,
         self.fiter,
         self.__doc__) = self.validate(*fargs, **fkwargs)

    def validate(self, *fargs, **fkwargs):
        fget, fset, fdel, fval, fitr, doc = self._validate_dispatch(*fargs, **fkwargs)
        if fitr is None:
            fitr = iter
        if doc is None and fget is not None:
            doc = fget.__doc__
        return fget, fset, fdel, fval, fitr, doc

    def _validate_dispatch(self, *fargs, **fkwargs):
        if len(fargs)==1 and len(fkwargs)==0:
            if inspect.isclass(fargs[0]):
                return self._validate_from_class(fargs[0])
        return self._validate_from_args(*fargs, **fkwargs)

    def _validate_from_args(self, fget=None, fset=None, fdel=None, fval=None, fitr=None, doc=None):
        """This is basically a validation function. Consider renaming?"""
        if fitr is None:
            fitr = iter
        if doc is None and fget is not None:
            doc = fget.__doc__
        return fget, fset, fdel, fval, fitr, doc

    def _validate_from_class(self, klass):
        kdict = vars(klass)
        fget = _grab(kdict, 'fget', '_get', 'getter', default=None)
        fset = _grab(kdict, 'fset', '_set', 'setter', default=None)
        fdel = _grab(kdict, 'fdel', '_del', 'deleter', default=None)
        fval = _grab(kdict, 'fval', '_val', 'validator', default=None)
        fitr = _grab(kdict, 'fiter', 'fitr', '_iter', 'iterator', default=iter)
        doc  = _grab(kdict, '__doc__', default=None)
        return fget, fset, fdel, fval, fitr, doc

    #----- Single-Target Descriptors (~not vectorized)
    def _get_(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)
    def _set_(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        if self.fval is not None: #Validate, if possible
            value = self.fval(obj, value)
        self.fset(obj, value)
    def _delete_(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    #----- Vectorized Descriptors
    def __get__(self, obj, objtype=None):
        return [self._get_(elm) for elm in obj]

    def __set__(self, obj, value):
        return [self._set_(elm, value) for elm in obj]

    def __delete__(self, obj):
        return [self._del_(elm) for elm in obj]

    #----- Decorators
    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.fval, self.__doc__)
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.fval, self.__doc__)
    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.fval, self.__doc__)
    def validator(self, fval):
        return type(self)(self.fget, self.fset, self.fdel, fval, self.__doc__)


class VectorMethod(VectorProperty):
    """The resulting method can be invoked - and maps invocation across elements."""
    def __get__(self, obj, objtype=None):
        return CallableMutableSequence([self._get_(elm) for elm in obj])

    def __set__(self, obj, value):
        return CallableMutableSequence([self._set_(elm, value) for elm in obj])

    def __delete__(self, obj):
        return CallableMutableSequence([self._del_(elm) for elm in obj])

class CallableMutableSequence(list):
    def __call__(self, *args, **kwargs):
        return [
            func(*args, **kwargs)
            for func in self
        ]

#==============================================================================
#    Local Utility Sections
#==============================================================================
def _grab(mapping, *keys, **kwargs):
    for key in keys:
        if key in mapping:
            return mapping[key]
    if 'default' in kwargs:
        return kwargs['default']
    else:
        raise KeyError('Could not find keys: '+', '.join(keys))
