from __future__ import absolute_import
import unittest

if __name__ == "__main__":
    from vector_property import *
else:
    from .vector_property import *


class Enumerant(object):
    def __init__(self, *cases):
        self.cases = cases
    def __iter__(self):
        return iter(self.cases)
    def __repr__(self):
        return repr(list(iter(self)))

class VectorPropertyTests(unittest.TestCase):
    def test_basic(self):
        class First(object):
            name = "Alpha"
            @classmethod
            def full_name(self):
                return self.name + " in the first degree."
        class Second(object):
            name = "Beta"
            @classmethod
            def full_name(self):
                return self.name + " for eternity."
        class Third(object):
            name = "Gamma"
            @classmethod
            def full_name(self):
                return self.name + " no unit or triad."

        class Group(Enumerant):
            @VectorProperty
            class name(object):
                def _get(self):
                    return self.name
            @VectorProperty
            class full_name(object):
                def _get(self):
                    return self.full_name

        mygroup = Group(First, Second, Third)

        self.assertEqual(mygroup.name, ['Alpha', 'Beta', 'Gamma'])
        self.assertEqual(
            [elm() for elm in mygroup.full_name],
            [
                'Alpha in the first degree.',
                'Beta for eternity.',
                'Gamma no unit or triad.'
            ]
        )        

    def test_sequence_of_dicts(self):
        first = {'a':1, 'b':2}
        second = {'a':3, 'b':4}
        third = {'a':5, 'b':6}

        class Atlas(Enumerant):
            @VectorProperty
            class aye(object):
                def _get(self):
                    return self['a']
                def _set(self, value):
                    self['a'] = value
                def _del(self):
                    del self['a']
            @VectorMethod
            class getitem(object):
                def _get(self):
                    return self.__getitem__
        myatlas = Atlas(first, second, third)

        self.assertEqual(myatlas.getitem('b'), [2, 4, 6])
        self.assertEqual(myatlas.aye, [1, 3, 5])        



if __name__ == "__main__":
    unittest.main()
