from zope.interface import implements
from zope.component import getUtility

from zope.schema import Set, Choice
from zope.schema import ValidationError

from zope.schema.interfaces import TooShort, TooLong

from plone.registry.interfaces import IRegistry

from collective.gtags.interfaces import ITags, ITagSettings
from collective.gtags.source import TagsSourceBinder
from collective.gtags.utils import split

from collective.gtags import MessageFactory as _

class TagsError(ValidationError):
    __doc__ = _(u"Invalid tags")
    
    def __init__(self, disallowed, nonunique, required):
        self.disallowed = disallowed
        self.nonunique = nonunique
        self.required = required

        # This is obscene... better solutions on a postcard, please.
        
        ids = ['tags_error']
        messages = []
        mapping = {}
        
        if self.disallowed:
            ids.append('disallowed')
            messages.append(u"Tags not allowed: ${disallowed}")
            mapping['disallowed'] = ', '.join(self.disallowed)
            
        if self.nonunique:
            ids.append('nonunique')
            messages.append(u"You may only have one tag in the following categories: ${nonunique}")
            mapping['nonunique'] = ', '.join(self.nonunique)
        
        if self.required:
            ids.append('required')
            messages.append(u"You must have at least one tag in the following categories: ${required}")
            mapping['required'] = ', '.join(self.required)
        
        self.error_message = _('_'.join(ids), default='; '.join(messages), mapping=mapping)

    def __str__(self):
        message = self.error_message
        
        default = message.default
        mapping = message.mapping
        
        for k, v in mapping.items():
            default = default.replace('${%s}' % k, v)
            
        return unicode(default)

class Tags(Set):
    """A field which may contain tags.
    """
    
    implements(ITags)
    
    validate_categories = True
    allow_uncommon = None
    
    def __init__(self, validate_categories=True, allow_uncommon=None, **kw):
        self.validate_categories = validate_categories
        self.allow_uncommon = allow_uncommon 
        
        # Avoid validation for the 'default' property, if set
        self._init_field = True
        super(Tags, self).__init__(**kw)
        self._init_field = False
        
        if self.value_type is None:
            self.value_type = Choice(
                    title=_(u"Tag"), 
                    source=TagsSourceBinder(allow_uncommon=allow_uncommon)
                )

    def _validate(self, tags):
        """Validate against the constraints in the nearest ITagSettings
        utility
        """
        
        # Skip validation during field initialisation
        if self._init_field:
            return
        
        if self.min_length is not None and len(tags) < self.min_length:
            raise TooShort(tags, self.min_length)

        if self.max_length is not None and len(tags) > self.max_length:
            raise TooLong(tags, self.max_length)
        
        if not self.required and not tags:
            return
        
        settings = getUtility(IRegistry).forInterface(ITagSettings)
        
        allowed_tags = set(settings.tags)
        unique_categories = set(settings.unique_categories)
        required_categories = set(settings.required_categories)
        
        categories_used = {}
        
        disallowed = set()
        nonunique = set()
        required = set()
        
        if self.allow_uncommon is not None:
            allow_uncommon = self.allow_uncommon
        else:
            allow_uncommon = settings.allow_uncommon
        
        for tag in tags:
            category, value = split(tag)
            
            if not allow_uncommon and tag not in allowed_tags:
                disallowed.add(tag)
                
            if self.validate_categories and category is not None:
                if category in categories_used and category in unique_categories:
                    nonunique.add(category)
                categories_used.setdefault(category, []).append(tag)
        
        if self.validate_categories:
            for category in required_categories:
                if category not in categories_used:
                    required.add(category)
                else:
                    found = False
                    for tag in categories_used[category]:
                        if tag in allowed_tags:
                            found = True
                            continue
                    if not found:
                        required.add(category)
        
        if disallowed or nonunique or required:
            raise TagsError(disallowed, nonunique, required)