from __future__ import absolute_import
import inspect
import collections
if __name__ == "__main__":
    from tryget import _trygetter, NotPassed
else:
    from .tryget import _trygetter, NotPassed

__all__ = ['VProperty', 'FProperty']





class VProperty(object):
    """Enchanced Python property, supporting 
    
    @TODO: Allow the function names for the class to be specified as
        either 'fget'/'getter', 'fset'/'setter', 'fdel'/'deleter', 'fval'/'validator'
    @TODO: Allow additional methods to be provided on a decorated class. Essentially
        anything not causing a conflict. basically I would like the class defined in
        the decorator to be in the method-resolution order for the new vproperty descriptor.
        (* complication: need to rename getter/setter/deleter/validator to fget/fset etc)
    @TODO: Consider having the names on the class be:
        '_get', '_set', '_del', '_validate' - so that pylint doesn't complain about them.
    
    """
    def __init__(self, *fargs, **fkwargs):
        """Check if used as a decorator for a class, or if used
        conventionally.
        """
        arguments = self.validate(*fargs, **fkwargs)
            
        (self.fget,
         self.fset,
         self.fdel,
         self.fval,
         self.__doc__) = arguments
         
    def validate(self, *fargs, **fkwargs):
        fget, fset, fdel, fval, doc = self._validate_dispatch(*fargs, **fkwargs)
        if doc is None and fget is not None:
            doc = fget.__doc__
        return fget, fset, fdel, fval, doc

        
    def _validate_dispatch(self, *fargs, **fkwargs):
        if len(fargs)==1 and len(fkwargs)==0:
            if inspect.isclass(fargs[0]):
                return self._validate_from_class(fargs[0])
        return self._validate_from_args(*fargs, **fkwargs)
    def _validate_from_args(self, fget=None, fset=None, fdel=None, fval=None, doc=None):
        """This is basically a validation function. Consider renaming?"""
        if doc is None and fget is not None:
            doc = fget.__doc__
        return fget, fset, fdel, fval, doc
    def _validate_from_class(self, klass):
        fget = TryGetAttr(klass, ('fget', '_get', 'getter'), default=None)
        fset = TryGetAttr(klass, ('fset', '_set', 'setter'), default=None)
        fdel = TryGetAttr(klass, ('fdel', '_del', 'deleter'), default=None)
        fval = TryGetAttr(klass, ('fval', '_val', 'validator'), default=None)
        doc  = TryGetAttr(klass, '__doc__', default=None)        
        return fget, fset, fdel, fval, doc
    #----- Descriptors
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        if self.fval is not None: #Validate, if possible
            value = self.fval(obj, value)
        self.fset(obj, value)
#         if self.fval is None:
#             self.fset(obj, value)
#         else:
#             self.fset(obj, self.fval(obj, value))
    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)
    #----- Decorators
    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.fval, self.__doc__)
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.fval, self.__doc__)
    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.fval, self.__doc__)
    def validator(self, fval):
        return type(self)(self.fget, self.fset, self.fdel, fval, self.__doc__)



#class FProperty(property)
# -- would like, but it creates problems with read-only
class FProperty(object):
    """Enhanced class-based property."""
    def __init__(self, *fargs, **fkwargs):
        """
        """
        arguments = self.validate(*fargs, **fkwargs)
            
        (self.fget,
         self.fset,
         self.fdel,
         self.fval,
         self.__doc__) = arguments
         

    #----- Descriptors
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)        
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        if self.fval is not None: #Validate, if possible
            value = self.fval(obj, value)
        self.fset(obj, value)
    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)
    #----- Decorators
    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.fval, self.__doc__)
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.fval, self.__doc__)
    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.fval, self.__doc__)
    def validator(self, fval):
        return type(self)(self.fget, self.fset, self.fdel, fval, self.__doc__)
    
    #------ Input Validation
    # ... probably unnecssarily complicated
    def validate(self, *fargs, **fkwargs):
        """Dispatch. Check if used as a decorator for a class, or if used
        conventionally, then validate inputs.
        """
        fget, fset, fdel, fval, doc = self._validate_dispatch(*fargs, **fkwargs)
        if doc is None and fget is not None:
            doc = fget.__doc__
        self._validate_typecheck(fget, fset, fdel, fval, doc)
        return fget, fset, fdel, fval, doc
        
    def _validate_dispatch(self, *fargs, **fkwargs):
        if len(fargs)==1 and len(fkwargs)==0:
            if inspect.isclass(fargs[0]):
                return self._validate_from_class(fargs[0])
        return self._validate_from_args(*fargs, **fkwargs)
    
    def _validate_from_args(self, fget=None, fset=None, fdel=None, fval=None, doc=None):
        """This is basically a validation function. Consider renaming?"""
        if doc is None and fget is not None:
            doc = fget.__doc__
        return fget, fset, fdel, fval, doc

    def _validate_from_class(self, klass):
        fget = TryGetAttr(klass, ['fget', '_get', 'getter'], default=None)
        fset = TryGetAttr(klass, ['fset', '_set', 'setter'], default=None)
        fdel = TryGetAttr(klass, ['fdel', '_del', 'deleter'], default=None)
        fval = TryGetAttr(klass, ['fval', '_val', 'validator'], default=None)
        doc  = TryGetAttr(klass, ['__doc__'], default=None)
        if doc is None and fget is not None:
            doc = fget.__doc__
        return fget, fset, fdel, fval, doc
    
    def _validate_typecheck(self, fget, fset, fdel, fval, doc):
        fget = self._validate_typecheck_func(fget, 'fget')
        fset = self._validate_typecheck_func(fset, 'fset')
        fdel = self._validate_typecheck_func(fdel, 'fdel')
        fval = self._validate_typecheck_func(fval, 'fval')
        if not isinstance(doc, (basestring, type(None))):
            raise TypeError("'doc' must be basestring or NoneType")
        
    def _validate_typecheck_func(self, farg, name):
        if not isinstance(farg, (collections.Callable, type(None))):
            raise TypeError("'{0}' must be Callable or NoneType.".format(name))
        return farg
            






#==============================================================================
#    Local Utility Sections
#==============================================================================
def _trygetpure(associations, indexes, default=NotPassed):
    getter = lambda assoc, index: object.__getattribute__(assoc, index)
    return _trygetter(getter, associations, indexes, default=default)

def _tryget(klass, attributes, **kwargs):
    """Return the first attribute from among 'attributes' which is found inside
    'klass'. If 'default' provided, then that is returned if none of the 
    attributes is found.
     
    Note: object.__getattribute__(klass, attr), returns a subtly
    different object than getattr(klass, attr).
    The first will return a function, and the second an unbound method.
    """
    if isinstance(attributes, basestring):
        attributes = [attributes]
    assert(isinstance(attributes, collections.Sequence))
         
    for attr in attributes:
        try:
            return object.__getattribute__(klass, attr)
        except AttributeError:
            pass
    if 'default' in kwargs:
        return kwargs['default']
    else:
        raise AttributeError("Could not find any of the attributes: "+str(attrs))

# def _defaults(*mappings):
#     """Handles defaults for sequence of mappings (~dicts).
#     The first (left-most) mapping is the highest priority."""
#     return dict(
#         (k, v)
#         for mapping in reversed(mappings)
#         for k, v in mapping.items()
#     )
        
        
def invoke_property(klass):
    return klass()

def call(*args, **kwargs):
    """Decorator. Call function using provided arguments."""
    def outer(func):
        return func(*args, **kwargs)
    return outer