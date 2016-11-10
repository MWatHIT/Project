# -*- coding: utf-8 -*-
from interfaces import ISQLAlchemyConnectionStrings
from persistent.mapping import PersistentMapping
from UserDict import DictMixin
from zope.annotation.interfaces import IAnnotatable
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import implementer
from zope.lifecycleevent import modified

ANNKEY = 'collective.saconnect.storage'


@implementer(ISQLAlchemyConnectionStrings)
@adapter(IAnnotatable)
class SQLAlchemyConnectionStrings(DictMixin):

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)
        self._dict = annotations.setdefault(ANNKEY, PersistentMapping())

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise ValueError('Only plain ascii keys are accepted')
        if not isinstance(value, str):
            raise ValueError('Only plain ascii values are accepted')
        self._dict[key] = value
        modified(self, key)

    def __delitem__(self, key):
        del self._dict[key]
        modified(self, key)

    def keys(self):
        return self._dict.keys()
