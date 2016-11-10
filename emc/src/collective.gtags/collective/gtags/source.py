# -*- coding: utf-8 -*-
import urllib
from binascii import b2a_qp
from zope.interface import implements,implementer
from zope.component import getUtility
from Products.CMFPlone.utils import safe_unicode

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import IVocabularyFactory

from plone.registry.interfaces import IRegistry

from z3c.formwidget.query.interfaces import IQuerySource

from collective.gtags.interfaces import ITagSettings

class TagsSource(object):
    implements(IQuerySource)

    def __init__(self, context, allow_uncommon=None):
        settings = getUtility(IRegistry).forInterface(ITagSettings)
        
        if allow_uncommon is None:
            self.allow_uncommon = settings.allow_uncommon
        else:
            self.allow_uncommon = allow_uncommon

        self.vocab = SimpleVocabulary.fromItems([
                (self._quote(value), unicode(value)) for value in settings.tags
            ])
    
    def __contains__(self, value):
        
        # If we allow uncommon terms, then anything is in the vocabulary
        if self.allow_uncommon:
            return True
        
        return self.vocab.__contains__(value)
        
    def __iter__(self):
        return self.vocab.__iter__()
    
    def __len__(self):
        return self.vocab.__len__()
    
    def getTerm(self, value):
        if self.allow_uncommon:
            return SimpleTerm(value=value, token=self._quote(value))
        else:
            return self.vocab.getTerm(value)
    
    def getTermByToken(self, token):
        if self.allow_uncommon:
            return SimpleTerm(value=self._unquote(str(token)), token=token)
        else:
#  old           return self.vocab.getTermByToken(token)
            return self.vocab.getTermByToken(self._quote(token))
    
    def search(self, query_string):
        q = query_string.lower()
        return [term for term in self.vocab if q in term.token.lower()]
    
    def _quote(self, value):
        return urllib.quote_plus(value.encode('utf-8', 'ignore'))
    
    def _unquote(self, token):
        return unicode(urllib.unquote_plus(token), encoding='utf-8')
    
class TagsSourceBinder(object):
    implements(IContextSourceBinder)

    def __init__(self, allow_uncommon=None):
        self.allow_uncommon = allow_uncommon

    def __call__(self, context):
        return TagsSource(context, self.allow_uncommon)
    
        
    
@implementer(IVocabularyFactory)
class KeywordsVocabulary(object):
    """Vocabulary factory listing all catalog keywords from the "Subject" index

        >>> from plone.app.vocabularies.tests.base import DummyCatalog
        >>> from plone.app.vocabularies.tests.base import create_context
        >>> from plone.app.vocabularies.tests.base import DummyContent
        >>> from plone.app.vocabularies.tests.base import Request
        >>> from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex  # noqa

        >>> context = create_context()

        >>> rids = ('/1234', '/2345', '/dummy/1234')
        >>> tool = DummyCatalog(rids)
        >>> context.portal_catalog = tool
        >>> index = KeywordIndex('Subject')
        >>> done = index._index_object(
        ...     1,
        ...     DummyContent('ob1', ['foo', 'bar', 'baz']), attr='Subject'
        ... )
        >>> done = index._index_object(
        ...     2,
        ...     DummyContent(
        ...         'ob2',
        ...         ['blee', 'bar', 'non-\xc3\xa5scii']),
        ...         attr='Subject',
        ... )
        >>> tool.indexes['Subject'] = index
        >>> vocab = KeywordsVocabulary()
        >>> result = vocab(context)
        >>> result.by_token.keys()
        ['blee', 'baz', 'foo', 'bar', 'non-=C3=A5scii']
        >>> result.getTermByToken('non-=C3=A5scii').title
        u'non-\\xe5scii'

        Testing unicode vocabularies
        First clear the index. Comparing non-unicode to unicode objects fails.
        >>> index.clear()
        >>> done = index._index_object(
        ...     1,
        ...     DummyContent('obj1', [u'äüö', u'nix']), attr="Subject"
        ... )
        >>> tool.indexes['Subject'] = index
        >>> vocab = KeywordsVocabulary()
        >>> result = vocab(context)
        >>> result.by_token.keys()
        ['nix', '=C3=83=C2=A4=C3=83=C2=BC=C3=83=C2=B6']
        >>> result.by_value.keys() == [u'äüö', u'nix']
        True
        >>> test_title = result.getTermByToken(
        ...     '=C3=83=C2=A4=C3=83=C2=BC=C3=83=C2=B6'
        ... ).title
        >>> test_title == u'äüö'
        True

    """
    # Allow users to customize the index to easily create
    # KeywordVocabularies for other keyword indexes
    

    def __call__(self, context, query=None):

        settings = getUtility(IRegistry).forInterface(ITagSettings)
        tags = settings.tags
        if tags is None:
            return SimpleVocabulary([])
        
        def safe_encode(term):
            if isinstance(term, unicode):
                # no need to use portal encoding for transitional encoding from
                # unicode to ascii. utf-8 should be fine.
                term = term.encode('utf-8')
            return term

        # Vocabulary term tokens *must* be 7 bit values, titles *must* be
        # unicode
        newtags = map(safe_encode,tags)
        items = [
            SimpleTerm(i, b2a_qp(i), safe_unicode(i))
            for i in newtags
            if query is None or safe_encode(query) in i
        ]
        return SimpleVocabulary(items)

KeywordsVocabularyFactory = KeywordsVocabulary()    