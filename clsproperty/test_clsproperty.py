from __future__ import absolute_import
import unittest

if __name__ == "__main__":
    from clsproperty import *
else:
    from .clsproperty import *


class FPropertyTests(unittest.TestCase):
    def setUp(self):
        pass
 
    def test_class_input(self):
        class MyClass(object):
            def __init__(self, bar=None):
                if not bar is None:
                    self.bar = bar
            @FProperty
            class bar(object):
                def _get(self):                    
                    if not hasattr(self, '_bar'):
                        self._bar = 'boo-bar-baz'
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
         
        myinst = MyClass()
        self.assertEqual(myinst.bar, 'boo-bar-baz')
        myinst.bar = 'bingo'
        self.assertEqual(myinst.bar, 'bingo')
        self.assertRaises(TypeError, lambda: setattr(myinst, 'bar', 5))
         
        del myinst.bar
        self.assert_(not hasattr(myinst, '_bar'))
        self.assertEqual(myinst.bar, 'boo-bar-baz')
        self.assert_(hasattr(myinst, '_bar'))
        
    def test_argument_input(self):
        class MyClass(object):
            def __init__(self, bar=None):
                if not bar is None:
                    self.bar = bar
            @FProperty
            def bar(self):
                if not hasattr(self, '_bar'):
                    self._bar = 'boo-bar-baz'
                return self._bar
            @bar.setter
            def bar(self, value):
                self._bar = value
            @bar.deleter
            def bar(self):
                del self._bar
            @bar.validator
            def bar(self, value):
                if not isinstance(value, str):
                    raise TypeError("'bar' must be 'str'.")
                return value

        myinst = MyClass()
        self.assertEqual(myinst.bar, 'boo-bar-baz')        
        myinst.bar = 'bingo'
        self.assertEqual(myinst.bar, 'bingo')
        self.assertRaises(TypeError, lambda: setattr(myinst, 'bar', 5))
        
        del myinst.bar
        self.assert_(not hasattr(myinst, '_bar'))
        self.assertEqual(myinst.bar, 'boo-bar-baz')
        self.assert_(hasattr(myinst, '_bar'))

class VPropertyTests(unittest.TestCase):
    def setUp(self):
        self.init_val = 'bar'
        self.set_val = 'foo'
         
    def basic_property_tests(self, Klass):
        myobj = Klass()
        #Setter
        myobj.data = self.set_val
        self.assertEquals(myobj._data, self.set_val)
        #Getter
        self.assertEquals(myobj.data, self.set_val)
        #Deleter
        del myobj.data
        self.assertRaises(AttributeError, lambda: myobj.data)
        self.assert_(not hasattr(myobj, 'data'))
        self.assert_(not hasattr(myobj, '_data'))
 
          
    def extended_property_tests(self, Klass):
        myobj = Klass()
        #Validator
        self.assertRaises(AssertionError, lambda: setattr(myobj, 'data', 123))
         
    def test_class_decorator(self):
        class MyClass(object):
            def __init__(self):
                pass
            @VProperty
            class data(object):
                """This is the property 'data' for 'MyClass'."""
                def getter(self):
                    return self._data
                def setter(self, value):
                    self._data = value
                def deleter(self):
                    del self._data
                def validator(self, value):
                    assert(isinstance(value, basestring))
                    return value
        self.basic_property_tests(MyClass)
        self.extended_property_tests(MyClass)
 
    def test_method_decorator(self):
        class MyClass(object):
            def __init__(self):
                pass
            @VProperty
            def data(self):
                return self._data
            @data.setter
            def data(self, value):
                self._data = value
            @data.deleter
            def data(self):
                del self._data
            @data.validator
            def data(self, value):
                assert(isinstance(value, basestring))
                return value
        self.basic_property_tests(MyClass)
        self.extended_property_tests(MyClass)
     
    def test_function_decorator(self):
        def Assertion(val):
            assert(val)
              
        class MyClass(object):
            def __init__(self):
                pass
            data = VProperty(
                lambda self: getattr(self, '_data'),
                lambda self, value: setattr(self, '_data', value),
                lambda self: delattr(self, '_data'),
                lambda self, value: value if isinstance(value, basestring) else Assertion(False),
            )
        self.basic_property_tests(MyClass)
        self.extended_property_tests(MyClass)


class SPropertyTests(unittest.TestCase):
    def setUp(self):
        self.init_val = 'bar'
        self.set_val = 'foo'
         
    def basic_property_tests(self, Klass):
        myobj = Klass()
        
        #Setter
        myobj.data = self.set_val
        self.assertEquals(myobj._data, self.set_val)
        #Getter
        self.assertEquals(myobj.data, self.set_val)
        #Deleter
        del myobj.data
        self.assertRaises(AttributeError, lambda: myobj.data)
        self.assert_(not hasattr(myobj, 'data'))
        self.assert_(not hasattr(myobj, '_data'))
 

        
    def test_class_decorator(self):
        class MyClass(object):
            def __init__(self):
                pass
            @SProperty
            class data(object):
                """This is the property 'data' for 'MyClass'."""
                def getter(self):
                    return self._data
                def setter(self, value):
                    self._data = value
                def deleter(self):
                    del self._data

        self.basic_property_tests(MyClass)

    def test_property(self):
        class MyKlass(object):
            def __init__(self):
                pass
            @SProperty
            def data(self):
                return self._data
            @data.setter
            def data(self, value):
                self._data = value
            @data.deleter
            def data(self):
                del self._data
 
        self.basic_property_tests(MyKlass)


if __name__ == "__main__":
    unittest.main()