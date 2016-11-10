# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone.memoize import ram
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
import json


def __call__(self, domain, language=None):
        if domain is None:
            return
        if language is None:
            language = self.request['LANGUAGE']

        tp = language.split("-")
        if len(tp) > 1:
            language = "%s_%s" % (tp[0],tp[1].upper())
        
        catalog = self._gettext_catalog(domain, language)
        response = self.request.response
        response.setHeader('content-type', 'application/json')
        response.setBody(json.dumps(catalog))
        return response