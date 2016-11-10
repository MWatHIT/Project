from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from five import grok
from zope.schema.interfaces import IVocabularyFactory
#import unicodedata

from emc.bokeh import _


source_type=[    ('inline','inline',_(u'inline')),
                  ('upload','upload',_(u'upload')),
                  ('reference','reference',_(u'reference')),
                        ]
source_type_terms = [SimpleTerm(value, token, title) for value, token, title in source_type ]

class SourceType(object):

    def __call__(self, context):
        return SimpleVocabulary(source_type_terms)

grok.global_utility(SourceType, IVocabularyFactory,
        name="emc.bokeh.vocabulary.sourcetype")

axis_type=[    ('linear','linear',_(u'Linear coordinate')),
                  ('log','log',_(u'logarithmic coordinate')),
                  ('datetime','date',_(u'Date time')),
                        ]
axis_type_terms = [SimpleTerm(value, token, title) for value, token, title in axis_type ]

class AxisType(object):

    def __call__(self, context):
        return SimpleVocabulary(axis_type_terms)

grok.global_utility(AxisType, IVocabularyFactory,
        name="emc.bokeh.vocabulary.axistype")