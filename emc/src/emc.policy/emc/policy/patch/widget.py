# -*- coding: utf-8 -*-
from Acquisition import ImplicitAcquisitionWrapper
from UserDict import UserDict
from Products.CMFCore.utils import getToolByName
from lxml import etree
from plone.app.textfield.value import RichTextValue
from plone.app.textfield.widget import RichTextWidget as patextfield_RichTextWidget
from plone.app.widgets.base import InputWidget
from plone.app.widgets.base import SelectWidget as BaseSelectWidget
from plone.app.widgets.base import TextareaWidget
from plone.app.widgets.base import dict_merge
from plone.app.widgets.utils import NotImplemented
from plone.app.widgets.utils import get_ajaxselect_options
from plone.app.widgets.utils import get_date_options
from plone.app.widgets.utils import get_datetime_options
from plone.app.widgets.utils import get_querystring_options
from plone.app.widgets.utils import get_relateditems_options
from plone.app.widgets.utils import get_tinymce_options
from plone.app.widgets.utils import get_widget_form
from plone.registry.interfaces import IRegistry
from plone.app.z3cform.utils import closest_content
from z3c.form.browser.select import SelectWidget as z3cform_SelectWidget
from z3c.form.browser.text import TextWidget as z3cform_TextWidget
from z3c.form.browser.widget import HTMLInputWidget
from z3c.form.interfaces import IEditForm
from z3c.form.interfaces import IForm
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import NO_VALUE
from z3c.form.widget import FieldWidget
from z3c.form.widget import Widget
from zope.component import getUtility
from zope.component import ComponentLookupError
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import implementsOnly
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import ISequence
from plone.app.widgets.utils import first_weekday

from plone.app.z3cform.converters import (
    DateWidgetConverter, DatetimeWidgetConverter)
from plone.app.z3cform.interfaces import (
    IDatetimeWidget, IDateWidget, IAjaxSelectWidget,
    IRelatedItemsWidget, IQueryStringWidget, IRichTextWidget,
    ISelectWidget)

import json

from Products.CMFPlone.interfaces import IEditingSchema
from plone.app.z3cform.widget import RichTextWidget

def _base_args(self):
        args = super(RichTextWidget, self)._base_args()

        args['name'] = self.name
        value = self.value and self.value.raw_encoded or ''
        args['value'] = (self.request.get(
            self.field.getName(), value)).decode('utf-8')

        args.setdefault('pattern_options', {})
        merged_options = dict_merge(get_tinymce_options(self.context,
                                                        self.field,
                                                        self.request),  # noqa
                                    args['pattern_options'])
        args['pattern_options'] = merged_options
        if args['name'] == "form.widgets.IRichText.report":
            args['pattern_options']['tiny']['height'] = 150
            

        return args