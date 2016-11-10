# -*- coding: utf-8 -*-
import unittest
import os
import os.path
from zope import event
from zope.interface import alsoProvides
from zope.component import createObject
from zope.component import queryUtility

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser

from plone.app.contenttypes.interfaces import IFile
from emc.bokeh.content.code2plot import ICodeFile

from emc.bokeh.testing import (
    PLONE_APP_CONTENTTYPES_INTEGRATION_TESTING,
    PLONE_APP_CONTENTTYPES_FUNCTIONAL_TESTING
)

from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.z3cform.interfaces import IPloneFormLayer

from plone.namedfile.file import NamedFile
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from collective.filepreviewbehavior.events import PreviewableFileCreatedEvent
from plone.namedfile.file import NamedBlobFile

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'rb')

class FileIntegrationTest(unittest.TestCase):

    layer = PLONE_APP_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(
            IDexterityFTI,
            name='emc.bokeh.codefile')
        schema = fti.lookupSchema()
        self.assertEqual(schema.getName(), 'plone_0_emc_2_bokeh_2_codefile')

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name='emc.bokeh.codefile'
        )
        self.assertNotEquals(None, fti)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='emc.bokeh.codefile'
        )
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IFile.providedBy(new_object))

    def test_adding(self):
        self.portal.invokeFactory(
            'emc.bokeh.codefile',
            'doc1'
        )
        self.assertTrue(ICodeFile.providedBy(self.portal['doc1']))

    def test_view(self):
        self.portal.invokeFactory('emc.bokeh.codefile', 'file')
        file1 = self.portal['file']
        file1.title = "My File"
        file1.description = "This is my file."
        data = getFile('temp.py').read()
        file1.file = NamedBlobFile(data,"application/x-python-code",u"temp.py")
        import pdb
        pdb.set_trace()
#         file1.file.data = data
        event.notify(PreviewableFileCreatedEvent(file1))
        self.request.set('URL', file1.absolute_url())
        self.request.set('ACTUAL_URL', file1.absolute_url())
        alsoProvides(self.request, IPloneFormLayer)
        view = file1.restrictedTraverse('@@view')

        self.assertTrue(view())
        self.assertEqual(view.request.response.status, 200)
        self.assertTrue('My File' in view())
        self.assertTrue('This is my file.' in view())






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

    def test_add_pyfile(self):
        self.browser.open(self.portal_url)

        self.browser.getLink('CodeFile').click()
        self.browser.getControl(name='form.widgets.title')\
            .value = "My file"
        self.browser.getControl(name='form.widgets.description')\
            .value = "This is my file."
        file_path = os.path.join(os.path.dirname(__file__), "temp.py")
        file_ctl = self.browser.getControl(name='form.widgets.file')
        file_ctl.add_file(open(file_path), 'image/png', 'temp.py')
        self.browser.getControl('Save').click()
        self.assertTrue(self.browser.url.endswith('temp.py/view'))
        self.assertTrue('My file' in self.browser.contents)
        self.assertTrue('This is my file' in self.browser.contents)





