from plone.app.registry.browser import controlpanel

from collective.gtags.interfaces import ITagSettings
from collective.gtags import MessageFactory as _

try:
    # only in z3c.form 2.0
    from z3c.form.browser.textlines import TextLinesFieldWidget
except ImportError:
    from plone.z3cform.textlines import TextLinesFieldWidget

class TagSettingsEditForm(controlpanel.RegistryEditForm):
    
    schema = ITagSettings
    label = _(u"Tagging settings") 
    description = _(u"Please enter details of available tags")
    
    def updateFields(self):
        super(TagSettingsEditForm, self).updateFields()
        self.fields['tags'].widgetFactory = TextLinesFieldWidget
        self.fields['unique_categories'].widgetFactory = TextLinesFieldWidget
        self.fields['required_categories'].widgetFactory = TextLinesFieldWidget
    
    def updateWidgets(self):
        super(TagSettingsEditForm, self).updateWidgets()
        self.widgets['tags'].rows = 8
        self.widgets['tags'].style = u'width: 30%;'
        self.widgets['unique_categories'].rows = 8
        self.widgets['unique_categories'].style = u'width: 30%;'
        self.widgets['required_categories'].rows = 8
        self.widgets['required_categories'].style = u'width: 30%;'
    
class TagSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = TagSettingsEditForm