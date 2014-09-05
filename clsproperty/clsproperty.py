




class FProperty(property):
    """Enhanced class-based property.
    
    
    class MyClass(object):
        def __init__(self, foo, bar):
            self.foo = foo
            print("I see self.bar == "+str(self.bar))
            self.bar = bar
        @invoke()
        class bar(SimpleProperty):
            def _get(self):
                if not hasattr(self, '_bar'):
                    self._bar = self.default
                return self._bar
            def _set(self, value):
                self._bar = value
            def _del(self):
                del self._bar
            def _val(self, value):
                if not isinstance(value, str):
                    raise TypeError("'bar' must be 'str'.")
                return value
            # Assign any extra traits you would like
            default = 'boo-bar-baz'
    
    @todo: Advanced - make this invoke() itself, using __new__ magic.
            
    """
    
    
    
    def __init__(self, *fargs, **fkwargs):
        """Check if used as a decorator for a class, or if used
        conventionally.
        """
        
        print(fargs, fkwargs)
        import pdb
        pdb.set_trace()
        print(fargs, fkwargs)
        
        arguments = self.validate(*fargs, **fkwargs)
            
        (self.fget,
         self.fset,
         self.fdel,
         self.fval,
         self.__doc__) = arguments
         
    def validate(self, *fargs, **fkwargs):
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
        print(klass.__dict__)
        import pdb
        pdb.set_trace()
        print(klass.__dict__)
        
        
        fget=_tryget(klass, '_get')
        fset=_tryget(klass, '_set')
        fdel=_tryget(klass, '_del')
        fval=_tryget(klass, '_val')
        doc=_tryget(klass, '__doc__')
        if doc is None and fget is not None:
            doc = fget.__doc__
        return fget, fset, fdel, fval, doc
    def _validate_from_mapping(self, mapping):
        trykey = lambda *keys: _trykey(mapping, keys, default=None)
        
        fget = trykey('fget', '_get', 'getter')
        fset = trykey('fset', '_set', 'setter')
        fdel = trykey('fdel', '_del', 'deleter')
        fval = trykey('fval', '_val', 'validator')
        doc  = trykey('__doc__')
        
        
        fget = _trykey(mapping, ('fget', '_get', 'getter'), default=None)
        fset = _trykey(mapping, ('fset','_set', ))
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



#==============================================================================
#    Local Utility Sections
#==============================================================================
def _tryget(klass, attributes, **kwargs):
    """Return the first attribute from among 'attributes' which is found inside
    'klass'. If 'default' provided, then that is returned if none of the 
    attributes is found.
    
    Note: object.__getattribute__(klass, attr), returns a subtly
    different object than getattr(klass, attr).
    The first will return a function, and the second an unbound method.
    """
    assert(
        isinstance(attributes, collections.Sequence) 
        and not isinstance(attributes, basestring)
    )
    for attr in attributes:
        try:
            return object.__getattribute__(klass, attr)
        except AttributeError:
            pass
    if 'default' in kwargs:
        return kwargs['default']
    else:
        raise AttributeError("Could not find any of the attributes: "+str(attrs))

def _trykey(mapping, keys, **kwargs):
    """Return the first attribute from among 'attributes' which is found inside
    'klass'. If 'default' provided, then that is returned if none of the 
    attributes is found.
    
    Note: object.__getattribute__(klass, attr), returns a subtly
    different object than getattr(klass, attr).
    The first will return a function, and the second an unbound method.
    """
    assert(isinstance(mapping, collections.Mapping))
    assert(isinstance(keys, collections.Iterable) and not isinstance(keys, str))
        
    for key in keys:
        try:
            return mapping[key]
        except KeyError:
            pass
    if 'default' in kwargs:
        return kwargs['default']
    else:
        raise KeyError("Could not find any of the attributes: "+str(keys))




def invoke_property(klass):
    return klass()

def call(*args, **kwargs):
    """Decorator. Call function using provided arguments."""
    def outer(func):
        return func(*args, **kwargs)
    return outer