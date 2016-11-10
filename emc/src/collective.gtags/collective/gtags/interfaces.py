from zope.interface import Interface, invariant, Invalid
from zope import schema

from zope.schema.interfaces import ISet

from z3c.form.interfaces import ISequenceWidget

from collective.gtags import MessageFactory as _

class InvalidCategories(Invalid):
    __doc__ = _(u"There must be a least one tag available for each category selected.")

class ITags(ISet):
    """A field containing a set of tags
    """
    
    validate_categories = schema.Bool(
            title=_(u"Validate categories"),
            description=_(u"Set to False to disable validation against globally "
                           "specified unique and required categories."),
            default=True,
            required=False,
        )
    
    allow_uncommon = schema.Bool(
            title=_(u"Allow uncommon tags"),
            description=_(u"If enabled, it will be possible to add "
                           "tags other than those in the pre-defined tags list"),
            required=False
        )

class ITagsWidget(ISequenceWidget):
    """A sequence of tags
    """

class ITagSettings(Interface):
    """A utility used to manage which tags are available and how categories
    are treated.
    """
    
    allow_uncommon = schema.Bool(
            title=_(u"Allow uncommon tags globally"),
            description=_(u"If enabled, it will be possible to add "
                           "tags other than those in the list below to "
                           "content objects that support this. If disabled, "
                           "all tags must be in the pre-defined list."),
            default=True,
            required=False,
        )
    
    tags = schema.Set(
            title=_(u"Pre-defined tags"),
            description=_(u"List pre-defined tags here. Tags can either be "
                            "simple strings or categorised using the form "
                            "Category-TagName."),
            required=True,
            default=set(),
            value_type=schema.TextLine(title=_(u"Tag")),
        )
        
    unique_categories = schema.Set(
            title=_(u"Unique categories"),
            description=_(u"If you want to ensure that users pick at most "
                            "one tag in a given category, list the category "
                            "name here."),
            required=True,
            default=set(),
            value_type=schema.TextLine(title=_(u"Category")),
        )

    required_categories = schema.Set(
            title=u"Required categories",
            description=_(u"If you want to ensure that users pick "
                            "at least one tag in a given category, "
                            "list the category name here."),
            required=True,
            default=set(),
            value_type=schema.TextLine(title=_(u"Category")),
        )
        
    @invariant
    def validate_categories_subset(obj):
        """Ensure that unique/required categories are a subset of the actual
        categories used in tags.
        """
        
        from collective.gtags.utils import get_categories
        
        tags = obj.tags
        if tags is None:
            tags = set()
        
        categories = get_categories(tags)
        if obj.unique_categories:
            for category in obj.unique_categories:
                if category not in categories:
                    raise InvalidCategories(_(u"${category} is not a valid category",
                                            mapping={'category': category}))
        
        if obj.required_categories:
            for category in obj.required_categories:
                if category not in categories:
                    raise InvalidCategories(_(u"${category} is not a valid category",
                                              mapping={'category': category}))