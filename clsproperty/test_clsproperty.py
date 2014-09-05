from __future__ import absolute_import
import unittest
if __name__ == "__main__":
    from clsproperty import *
else:
    from .clsproperty import *


class BasicTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic(self):
        class MyClass(object):
            def __init__(self, bar=None):
                if not bar is None:
                    self.bar = bar
            defaults = {
                'bar': 'boo-bar-baz'
            }
            @invoke_property
            class bar(FProperty):
                default = 'boo-bar-baz'
                def _get(self):
                    
                    print('--')
                    import pdb
                    pdb.set_trace()
                    print('--')
                    
                    if not hasattr(self, '_bar'):
                        self._bar = default
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
        
        print(myinst.bar)
        import pdb
        pdb.set_trace()
        print(myinst.bar)



if __name__ == "__main__":
    unittest.main()