"""Behaviours to assign tags (to ideas).

Includes a form field and a behaviour adapter that stores the data in the
standard Subject field.
"""

from rwproperty import getproperty, setproperty
from zope import schema
from zope.interface import implements, alsoProvides
from zope.component import adapts

from plone.directives import form
from plone.autoform import directives
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from collective.gtags.field  import Tags

from Products.CMFCore.interfaces import IDublinCore

from collective.gtags import MessageFactory as _

class ITags(form.Schema):
    """Add tags to content
    """
    
    form.fieldset(
            'categorization',
            label=_(u'Categorization'),
            fields=('tags',),
        )
    
    tags = Tags(
            title=_(u"Tags"),
            value_type=schema.TextLine(),
            description=_(u"Applicable tags"),
            required=False,
            allow_uncommon=False,
        )
    directives.widget(
        'tags',
        AjaxSelectFieldWidget,
        vocabulary='collective.gtags.Keywords'
    )

alsoProvides(ITags, form.IFormFieldProvider)

def filter_category(value):
    if "-" not in value:return value
    return value.split('-')[1]
        

class Tags(object):
    """Store tags in the Dublin Core metadata Subject field. This makes
    tags easy to search for.
    """
    implements(ITags)
    adapts(IDublinCore)

    def __init__(self, context):
        self.context = context
    
    @getproperty
    def tags(self):
        return set(self.context.Subject())
    @setproperty
    def tags(self, value):
        if value is None:
            value = ()
        # filter category
#         value = map(filter_category,value)            
        self.context.setSubject(tuple(value))
