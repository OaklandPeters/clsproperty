from __future__ import absolute_import
import unittest

if __name__ == "__main__":
    try:
        from tryget import _trygetattr, _trygetitem, _trygetter, NotPassed, TryGetError
    except ImportError:
        from clsproperty.tryget import _trygetattr, _trygetitem, _trygetter, NotPassed, TryGetError
else:
    from .tryget import _trygetattr, _trygetitem, _trygetter, NotPassed, TryGetError

class TestTryGet(unittest.TestCase):

    def test_TryGetAttr(self):
        class Klass1(object):
            def foo(self):  pass
            def bar(self):  pass
        class Klass2(object):
            def bar(self):  pass
            def baz(self):  pass

        self.assertEqual(
            TryGetAttr([Klass1, Klass2], 'bar'),
            Klass1.bar
            #Klass1.__dict__['bar']
        )
        self.assertEqual(
            TryGetAttr([Klass1, Klass2], 'foo'),
            Klass1.foo
        )
        self.assertEqual(
            TryGetAttr([Klass1, Klass2], 'baz'),
            Klass2.baz
        )
        self.assertRaises(
            AttributeError,
            lambda: TryGetAttr([Klass1, Klass2], 'bazinga')
        )
        
    def test_TryGetItem(self):
        mappings = ({'a':0,'b':1}, {'b':2,'c':3})
        self.assertEqual(
            TryGetItem(mappings, ('_a','a')),
            0
        )
        self.assertEqual(
            TryGetItem(mappings, ('_a','a','b')),
            0
        )
        self.assertEqual(
            TryGetItem(mappings, ('_a','b')),
            1
        )
        self.assertEqual(
            TryGetItem(mappings, 'b'),
            1
        )
        self.assertRaises(LookupError,
            lambda: TryGetItem(({'a':0,'b':1},{'b':2,'c':3}), ('__a'))
        )

        mixed = ({'a':0,'b':1},{'b':2,'c':3, 2:4}, (10,11,12,13))
        self.assertEqual(
            TryGetItem(mixed, ('_a', 1, 'a')),
            11
        )
        self.assertEqual(
            TryGetItem(mixed, ('_a', 6, 'a')),
            0
        )
        self.assertEqual(
            TryGetItem(mixed, 2),
            4
        )
        self.assertRaises(LookupError,
            lambda: TryGetItem(mixed, ('_a', 6))
        )
        self.assertRaises(LookupError,
            lambda: TryGetItem(mixed, '2')
        )

    def test_input_type_errors(self):
        pass







class Test_tryget(unittest.TestCase):

    def test__trygetattr(self):
        class Klass1(object):
            def foo(self):  pass
            def bar(self):  pass
        class Klass2(object):
            def bar(self):  pass
            def baz(self):  pass

        self.assertEqual(
            _trygetattr([Klass1, Klass2], 'bar'),
            Klass1.bar
        )
        self.assertEqual(
            _trygetattr([Klass1, Klass2], 'foo'),
            Klass1.foo
        )
        self.assertEqual(
            _trygetattr([Klass1, Klass2], 'baz'),
            Klass2.baz
        )
        self.assertRaises(
            TryGetError,
            lambda: _trygetattr([Klass1, Klass2], 'bazinga')
        )
        
    def test_trygetitem(self):
        mappings = ({'a':0,'b':1}, {'b':2,'c':3})
        self.assertEqual(
            _trygetitem(mappings, ('_a','a')),
            0
        )
        self.assertEqual(
            _trygetitem(mappings, ('_a','a','b')),
            0
        )
        self.assertEqual(
            _trygetitem(mappings, ('_a','b')),
            1
        )
        self.assertEqual(
            _trygetitem(mappings, 'b'),
            1
        )
        self.assertRaises(LookupError,
            lambda: _trygetitem(({'a':0,'b':1},{'b':2,'c':3}), ('__a'))
        )

        mixed = ({'a':0,'b':1},{'b':2,'c':3, 2:4}, (10,11,12,13))
        self.assertEqual(
            _trygetitem(mixed, ('_a', 1, 'a')),
            0
        )
        self.assertEqual(
            _trygetitem(mixed, ('_a', 6, 'a')),
            0
        )
        self.assertEqual(
            _trygetitem(mixed, 2),
            4
        )
        self.assertRaises(LookupError,
            lambda: _trygetitem(mixed, ('_a', 6))
        )
        self.assertRaises(LookupError,
            lambda: _trygetitem(mixed, '2')
        )

    def test_input_type_errors(self):
        pass

class TryGetterTests(unittest.TestCase):
    def test_imitiate_trygetattr(self):
        def _trygetimitation(associations, indexes, default=NotPassed):
            return _trygetter(getattr, associations, indexes, default=default)
        
        class Klass1(object):
            def foo(self):  pass
            def bar(self):  pass
        class Klass2(object):
            def bar(self):  pass
            def baz(self):  pass

        self.assertEqual(
            _trygetimitation([Klass1, Klass2], 'bar'),
            Klass1.bar
        )
        self.assertEqual(
            _trygetimitation([Klass1, Klass2], 'foo'),
            Klass1.foo
        )
        self.assertEqual(
            _trygetimitation([Klass1, Klass2], 'baz'),
            Klass2.baz
        )
        self.assertRaises(
            TryGetError,
            lambda: _trygetimitation([Klass1, Klass2], 'bazinga')
        )

    def test_imitate_trygetitem(self):
        def _trygetimitation(associations, indexes, default=NotPassed):
            getter = lambda assoc, index: assoc[index]
            return _trygetter(getter, associations, indexes, default=default)
        mappings = ({'a':0,'b':1}, {'b':2,'c':3})
        self.assertEqual(
            _trygetimitation(mappings, ('_a','a')),
            0
        )
        self.assertEqual(
            _trygetimitation(mappings, ('_a','a','b')),
            0
        )
        self.assertEqual(
            _trygetimitation(mappings, ('_a','b')),
            1
        )
        self.assertEqual(
            _trygetimitation(mappings, 'b'),
            1
        )
        self.assertRaises(LookupError,
            lambda: _trygetimitation(({'a':0,'b':1},{'b':2,'c':3}), ('__a'))
        )

        mixed = ({'a':0,'b':1},{'b':2,'c':3, 2:4}, (10,11,12,13))
        self.assertEqual(
            _trygetimitation(mixed, ('_a', 1, 'a')),
            0
        )
        self.assertEqual(
            _trygetimitation(mixed, ('_a', 6, 'a')),
            0
        )
        self.assertEqual(
            _trygetimitation(mixed, 2),
            4
        )
        self.assertRaises(LookupError,
            lambda: _trygetimitation(mixed, ('_a', 6))
        )
        self.assertRaises(LookupError,
            lambda: _trygetimitation(mixed, '2')
        )

if __name__ == "__main__":
    unittest.main()