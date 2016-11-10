from zope.interface import implementer, implementsOnly
from zope.component import getUtility

import z3c.form.interfaces
import z3c.form.widget
import z3c.form.error
import z3c.form.browser.widget

from plone.registry.interfaces import IRegistry

from collective.gtags.interfaces import ITagSettings, ITagsWidget
from collective.gtags.field import TagsError

class TagsErrorView(z3c.form.error.ErrorViewSnippet):
    
    def render(self):
        return self.context.error_message

z3c.form.error.ErrorViewDiscriminators(TagsErrorView, error=TagsError)

class TagsWidget(z3c.form.browser.widget.HTMLInputWidget, z3c.form.widget.SequenceWidget):
    """Widget for selecting tags
    """
    
    implementsOnly(ITagsWidget)

    klass = u'tags-widget'
    items = ()

    maxResults = 40
    minChars = 1
    numCols = 3

    def isChecked(self, term):
        return term.token in self.value

    def updateTerms(self):
        super(TagsWidget, self).updateTerms()
        self.normalized_tokens = {}
        for term in self.terms:
            self.normalized_tokens[term.token.strip().lower()] = term.token
    
    def update(self):
        super(TagsWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)
        
        self.settings = settings = getUtility(IRegistry).forInterface(ITagSettings)
        
        if self.field.allow_uncommon is not None:
            self.allow_uncommon = self.field.allow_uncommon
        else:
            self.allow_uncommon = settings
            
        self.validate_categories = self.field.validate_categories
        
    def rows(self):
        
        items = []
        
        # Find current tags
        
#         import pdb
#         pdb.set_trace()
        for count, tag in enumerate(sorted(self.value)):
            id = '%s-%i' % (self.id, count)
            items.append({
                    'id': id,
                    'name': self.name + ':list',
                    'value': tag,
                    'label': tag,
                })
    
        # Then add empty items to fill up a row
    
        num_items = len(items)
        
        num_rows = min((num_items / self.numCols) + 1, 2)
        total_items = num_rows * self.numCols
        
        num_missing = total_items - num_items
        for count in range(num_items, total_items):
            id = '%s-%i' % (self.id, count)
            items.append({
                    'id': id,
                    'name': self.name + ':list',
                    'value': '', 
                    'label': '',
                })
        
        # Arrange into rows and columns
        
        rows = []
        col = []
        for idx, item in enumerate(items):
            col.append(item)
            if (idx + 1) % self.numCols == 0:
                rows.append(col)
                col = []
        if col:
            rows.append(col)
            
        return rows
    
    def uncommon_tags(self):
    
        uncommon_tags = []
    
        # Find the items we actually have
        
        for tag in sorted(self.value):
            if tag not in self.settings.tags:
                uncommon_tags.append(tag)
        
        return uncommon_tags
    
    def extract(self, default=z3c.form.interfaces.NOVALUE):
#         import pdb
#         pdb.set_trace()
        if (self.name not in self.request and
            self.name+'-empty-marker' in self.request):
            return []
        
        value = self.request.get(self.name, default)
        if value == default:
            return default
        
        extracted = set()
        for token in value:
            if token == self.noValueToken:
                extracted.append(value)
            elif token:
                token = self.normalized_tokens.get(token.strip().lower(), token)
                try:
                    self.terms.getTermByToken(token)
                except KeyError:
                    return default
                
                extracted.add(token)
        return extracted
    
    def js(self):
        
        tags_array = self.to_js_array(self.settings.tags)
#         import pdb
#         pdb.set_trace()
        uncommon_tags_array = self.to_js_array(self.uncommon_tags())
        unique_categories_array = self.to_js_array(self.settings.unique_categories)
        required_categories_array = self.to_js_array(self.settings.required_categories)
        
        allow_uncommon_bool = str(self.allow_uncommon).lower()
        validate_categories_bool = str(self.validate_categories).lower()
        
        max_results_int = self.maxResults
        min_chars_int = self.minChars
        
        return """\
            (function($) {
                $().ready(function() {
                    
                    var id = '%(id)s';
                    var area = $('#' + id + '-area');
                    
                    var allow_uncommon = %(allow_uncommon_bool)s;
                    var validate_categories = %(validate_categories_bool)s;
                    
                    var tags_vocabulary = %(tags_array)s;
                    var unique_categories = %(unique_categories_array)s;
                    var required_categories = %(required_categories_array)s;
                    
                    var tags_lookup = new Object();
                    for (var i = 0; i < tags_vocabulary.length; ++i)
                        tags_lookup[tags_vocabulary[i]] = i;
                    
                    var unique_lookup = new Object();
                    for (var i = 0; i < unique_categories.length; ++i)
                        unique_lookup[unique_categories[i].toLowerCase()] = i;
                    
                    var autocomplete_options = {
                            autoFill: !allow_uncommon,
                            minChars: %(min_chars_int)d,
                            max: %(max_results_int)d,
                            mustMatch: !allow_uncommon,
                            matchContains: true,
                            multiple: false
                        };
                
                    function getCategory(tag) {
                        var parts = tag.split('-');
                        if(parts.length > 1) return parts[0];
                        else return null;
                    }
                    
                    function updateWarnings() {
                        var uncommon = new Array();

                        var required_lookup = new Object();
                        
                        if(validate_categories) {
                            for (var i = 0; i < required_categories.length; ++i)
                                required_lookup[required_categories[i].toLowerCase()] = required_categories[i];
                        }
                        
                        var categories_used = new Object();
                        var duplicates_detected = false;
                        
                        $('input[type=text]', area).each(function() {
                        
                            var tag = $(this).attr('value');
                            var category = getCategory(tag);
                            
                            if(tag != null && tag != '' && tags_lookup[tag] == null) {
                                uncommon.push(tag);
                            }
                            
                            if(validate_categories && category != null) {
                                var category_lower = category.toLowerCase();
                                
                                if(required_lookup[category_lower] != null) {
                                    delete required_lookup[category_lower];
                                }
                                
                                if(unique_lookup[category_lower] != null) {
                                    if(categories_used[category_lower] != null) {
                                        duplicates_detected = true;
                                    }
                                }
                                
                                categories_used[category_lower] = category;
                            }
                        });
                        
                        if(uncommon.length == 0) {
                            $('.uncommon-tag-warning', area).hide();
                            $('.uncommon-tags', area).empty();
                        } else {
                            $('.uncommon-tags', area).html(uncommon.join('; '));
                            $('.uncommon-tag-warning', area).show();
                        }
                        
                        if(validate_categories) {
                            if(duplicates_detected) {
                                $('.unique-categories-note', area).css('font-weight', 'bold');
                            } else {
                                $('.unique-categories-note', area).css('font-weight', 'normal');
                            }
                        
                            var required_left = Array();
                            for(var category in required_lookup)
                                required_left.push(required_lookup[category]);
                        
                            if(required_left.length == 0) {
                                $('.required-categories-note', area).css('font-weight', 'normal');
                            } else {
                                $('.required-categories-note', area).css('font-weight', 'bold');
                            }
                        }
                        
                    }
        
                    $('input[type=text]', area).each(function() {
                        $(this).autocomplete(tags_vocabulary, autocomplete_options);
                        $(this).change(updateWarnings);
                    });
            
                    $('.add-row-button', area).click(function(){
                        var lastrow = $('.tags-row:last', area);
                        var control_count = $('input[type=text]', area).size();
                
                        var newrow = lastrow.clone();
                        $('input[type=text]', newrow).each(function() {
                            $(this).attr('value', '')
                                   .attr('id', id + '-' + control_count++);
                            $(this).autocomplete(tags_vocabulary, autocomplete_options);
                            $(this).change(updateWarnings);
                        });

                        $(lastrow).after(newrow);
                
                        return false;
                    });
                });
            })(jQuery);
            """ % dict(
                    id=self.id,
                    allow_uncommon_bool=allow_uncommon_bool,
                    validate_categories_bool=validate_categories_bool,
                    tags_array=tags_array,
                    unique_categories_array=unique_categories_array,
                    required_categories_array=required_categories_array,
                    min_chars_int=self.minChars,
                    max_results_int=self.maxResults)

    def to_js_array(self, sequence):
        return "[%s]" % ', '.join(["'%s'" % i.replace("'", "\\'") for i in sequence])
    
@implementer(z3c.form.interfaces.IFieldWidget)
def TagsFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field, TagsWidget(request))