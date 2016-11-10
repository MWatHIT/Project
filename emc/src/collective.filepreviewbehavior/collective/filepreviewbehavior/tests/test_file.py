# -*- coding: utf-8 -*-
import unittest

import os.path

from zope.interface import alsoProvides
from zope.component import createObject
from zope.component import queryUtility
from zope.component import provideAdapter

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser

from plone.app.contenttypes.interfaces import IFile

from collective.filepreviewbehavior.testing import (
    PLONE_APP_CONTENTTYPES_INTEGRATION_TESTING,
    PLONE_APP_CONTENTTYPES_FUNCTIONAL_TESTING
)

from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.namedfile.file import NamedFile
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer

import os


def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')



class FileFunctionalTest(unittest.TestCase):

    layer = PLONE_APP_CONTENTTYPES_FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_alternative_mime_icon_doc_for_file(self):
        provideAdapter(AssignRoles)
        self.browser.open(self.portal_url)
        self.browser.getLink('File').click()

        self.browser.getControl(name='form.widgets.title')\
            .value = "My file"
        self.browser.getControl(name='form.widgets.description')\
            .value = "This is my doc file."
        file_path = os.path.join(os.path.dirname(__file__), "file.doc")
        file_ctl = self.browser.getControl(name='form.widgets.file')
        file_ctl.add_file(open(file_path), 'application/msword', 'file.doc')
        self.browser.getControl('Save').click()
        self.assertTrue(self.browser.url.endswith('file.doc/view'))
        self.assertTrue('custom.png' in self.browser.contents)


