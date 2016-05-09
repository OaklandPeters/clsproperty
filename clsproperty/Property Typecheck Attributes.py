
# coding: utf-8

# In[4]:


class TypeInfo(object):
    """
    @todo: Remake as instanceable class, using ValueMeta.
    """
    @classmethod
    def instancecheck(cls, typeinfo):
        """Is typeinfo valid for an isinstance call?
        IE a type, class, or tuple of types or classes?"""
        try:
            isinstance({}, typeinfo)
        except TypeError:
            return False
        return True
    @classmethod
    def names(cls, typeinfo):
        # Already assumes it is a valid typeinfo
        # assert(cls.instancecheck(typeinfo))
        if isinstance(typeinfo, tuple):
            return tuple([klass.__name__ for klass in typeinfo])
        else:
            return typeinfo.__name__
    @classmethod
    def _ensure_types(cls, typeinfo):
        """If not already valid type or tuple of types, then
        gets type of object (or type of each object in tuple).
        """
        if isinstance(typeinfo, tuple):
            return tuple(cls._ensure_types(elm) for elm in typeinfo)
        else:
            if isinstance(typeinfo, type):
                return obj
            else:
                return type(obj)
    exception = TypeError
    @classmethod
    def message(cls, typeinfo, name="object"):
        # Assumes typeinfo is invalid
        # assert(not cls.instancecheck(typeinfo))
        types_names = cls.names(cls._ensure_types(typeinfo))
        return str.format(
            "'{name}' must be a class, type or tuple of "
            "classes and types, not {types_names}.",
            name=name, types_names=types_names
        )
    @classmethod
    def validate(cls, typeinfo, name="object"):
        if not cls.instancecheck(typeinfo):
            raise cls.exception(
                cls.message(typeinfo, name=name)
            )
        return typeinfo

class Validator(object):
    __instancecheck__ = abc.abstractmethod()
    exception = abc.abstractproperty()
    message = abc.abstractmethod()
    def validate(self, obj, name="object"):
        if not self.__instancecheck__(obj):
            raise self.exception(
                self.message(obj, name=name)
            )
        return obj

def validate(obj, validator, name="object"):
    """Generic function"""
    if not isinstance(validator, Validator):
        raise TypeError("Not a validator.")
        
    if hasattr(validator, 'validate'):
        # Check to ensure that this hasn't looped back to this already
        return validator.validate(obj, name=name)
    
    if not validator.__instancecheck__(obj):
        raise validator.exception(
            validator.message(obj, name=name)
        )
    
    
    

class TypedProperty(property):
    """
    This was made into a class inheriting from property
    because the builtin 'property' object cannot have attributes
    added.
    """
    @property
    def valid_types(self):
        if not hasattr(self, '_valid_types'):
            self._valid_types = tuple()
        return self._valid_types
    @valid_types.setter
    def valid_types(self, value):
        self._valid_types = TypeInfo.validate(value)
    @valid_types.deleter
    def valid_types(self):
        del self._valid_types
    
    
            
class MyClass(object):
    def __init__(self, data):
        self.data = data
    @TypedProperty
    def data(self):
        if not hasattr(self, '_data'):
            self._data = None
        return self._data
    @data.setter
    def data(self, value):
        if hasattr(self, 'valid_types'):
            if not isinstance(value, self.valid_types):
                raise TypeError(
                )
        self._data = value

myinst = MyClass('argl')


# In[5]:

MyClass.data.typez = str


# In[7]:

isinstance("", None)


# In[ ]:



