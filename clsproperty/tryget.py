from __future__ import absolute_import
import collections
import abc



# Note: object.__getattribute__(klass, attr), returns a subtly
# different object than getattr(klass, attr).
# The first will return a function, and the second an unbound method.

# THIS WORKS:
# object.__getattribute__(assoc, index)
# <function _get at 0x2628aa0>
#
# THIS DOES NOT:
# object.__getattribute__(assoc, '__getattribute__')(index)
# <unbound method bar._get>

# getter = object.__getattribute__(assoc, '__getattribute__')


class TryGetInterface(object):
    """
    @todo: Have this use OperatorMeta instead of ABCMeta
    """
    __metaclass__ = abc.ABCMeta
    def __new__(cls, associations, indexes, **kwargs):
        return cls.__call__(associations, indexes, **kwargs)
    @classmethod
    def __call__(cls, associations, indexes, **kwargs):
        (associations, indexes, kwargs
            ) = cls.validate(associations, indexes, **kwargs)
        
        
            
        
        # main - try combinations of associations and indexes
        for index in indexes:
            for assoc in associations:                
                retriever = cls.get_retriever(assoc)        
                try:
                    return retriever(index)
                except cls.retriever_exceptions:
                    pass

        # No index was found - try default
        try:
            return kwargs['default']
        except KeyError:            
            raise cls.failure_exception(
                "Could not find any of the indexes: "+str(indexes)
            )
    #------------ Supporting functions
    @classmethod
    def validate(cls, associations, indexes, **kwargs):
        """Validate input arguments."""
        associations = _ensure_tuple(associations)
        indexes = _ensure_tuple(indexes)
        return associations, indexes, kwargs
#     @classmethod
#     def get_retriever(cls, assoc):
#         print(cls)
#         return getattr(assoc, cls.retriever_name)
    
    #------------ Abstract functions: required for interface
    retriever_name = abc.abstractproperty(lambda string: string) #string
    retriever_exceptions = abc.abstractproperty(lambda excs: excs) #exceptions
    failure_exception = abc.abstractproperty(lambda exc: exc) #exception

class TryGetAttr(TryGetInterface):
    retriever_name = '__getattribute__'
    retriever_exceptions = AttributeError
    failure_exception = AttributeError
    @classmethod
    def get_retriever(cls, assoc):
        return lambda index: assoc.__getattribute__(assoc, index)

class TryGetItem(TryGetInterface):
    retriever_name = '__getitem__'
    retriever_exceptions = (LookupError, TypeError)
    failure_exception = LookupError
    @classmethod
    def get_retriever(cls, assoc):
        return assoc.__getitem__
#     @classmethod
#     def retriever(cls, assoc, index):
#         return assoc[index]
    


#==============================================================================
#    Local Utility
#==============================================================================
def _ensure_tuple(obj):
    """Ensure that object is a tuple, or is wrapped in one. 
    Also handles some special cases.
    Tuples are unchanged; NonStringSequences and Iterators are converted into
    a tuple containing the same elements; all others are wrapped by a tuple.
    """
    #Tuples - unchanged
    if isinstance(obj, tuple):
        return obj
    #Sequences - convert to tuple containing same elements.
    elif isinstance(obj, collections.Sequence) and not isinstance(obj, basestring):
        return tuple(obj)
    #Iterators & Generators - consume into a tuple
    elif isinstance(obj, collections.Iterator):
        return tuple(obj)
    #Other Iterables, Strings, and non-Iterables - wrap in iterable first
    else:
        return tuple([obj])
