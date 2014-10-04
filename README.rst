clsproperty
============

Overview
--------
A simple tool which makes class properties a little more convenient and object-oriented than classical Python `property`.

Example
------------
Properties with clsproperty are constructed as a decorated nested class. The simplest decorator is `SProperty` (for 'simple property'), which defers almost all of it's operation to the builtin `property`. For example::

    from clsproperty import SProperty
    class MyClass(object):
        def __init__(self, bar=None):
            if not bar is None:
                self.bar = bar
        @SProperty
        class bar(object):
            """Documentation is attached to the class."""
            def _get(self):                    
                if not hasattr(self, '_bar'):
                    self._bar = 'boo-bar-baz'
                return self._bar
            def _set(self, value):
                self._bar = value
    
    obj = MyClass()
    assert obj.bar == 'boo-bar-baz'  #default value from _get
    obj.bar = 'foo'  #setter
    assert obj.bar == 'foo'

A slightly more advanced option is `VProperty` (for 'validating property'), which supplements standard property getter/setter/deleter with a `validator`, via the `fval` function. This function is ran on any assignment before passing it to the `fset` function - and is generally expected to raise an Exception for invalid inputs. For example::

    from clsproperty import SProperty, VProperty
    class MyClass(object):
        def __init__(self, bar=None):
            if not bar is None:
                self.bar = bar
        @VProperty
        class bar(object):
            """Documentation is attached to the class."""
            def _get(self):                    
                if not hasattr(self, '_bar'):
                    self._bar = 'boo-bar-baz'
                return self._bar
            def _set(self, value):
                self._bar = value
            def _del(self):
                del self._bar
            def _val(self, value):
                if not isinstance(value, basestring):
                    raise TypeError(str.format(
                        "'bar' must be a basestring, not {0}",
                        type(value).__name__
                    ))
                return value
    
    try:
        obj = MyClass(['foo','bar'])
    except TypeError as exc:
        assert(repr(exc)=="TypeError(\"'bar' must be a basestring, not list\",)")
    
    try:
        obj = MyClass('foo')
        obj.bar = 123
    except TypeError as exc:
        assert(repr(exc)=="TypeError(\"'bar' must be a basestring, not int\",)")


License
-----------
The MIT License (MIT)

Copyright (C) 2014, Oakland John Peters.