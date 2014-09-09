from __future__ import absolute_import
import unittest

from tryget import TryGetAttr, TryGetItem


class TestTryGet(unittest.TestCase):

    def test_trygetattr(self):
        class Klass1(object):
            def foo(self):  pass
            def bar(self):  pass
        class Klass2(object):
            def bar(self):  pass
            def baz(self):  pass

        self.assertEqual(
            TryGetAttr([Klass1, Klass2], 'bar'),
            Klass1.bar
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
            LookupError,
            lambda: TryGetAttr([Klass1, Klass2], 'bazinga')
        )
        
    def test_trygetitem(self):
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


if __name__ == "__main__":
    unittest.main()