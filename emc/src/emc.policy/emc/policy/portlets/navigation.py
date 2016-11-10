from Acquisition import aq_inner, aq_base, aq_parent
from ComputedAttribute import ComputedAttribute
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets import base
from plone.app.uuid.utils import uuidToObject
from plone.app.vocabularies.catalog import CatalogSource
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.interfaces import IBrowserDefault
from Products.CMFPlone import utils
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy
from Products.CMFPlone.defaultpage import is_default_page
from Products.CMFPlone.interfaces import INavigationSchema
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zExceptions import NotFound
from zope import schema
from zope.component import adapts, getMultiAdapter, queryUtility
from zope.component import getUtility
from zope.interface import implements, Interface

from plone.app.portlets.portlets.navigation import INavigationPortlet
from plone.app.portlets.portlets.navigation import Assignment
from plone.app.portlets.portlets.navigation import  Renderer as baseRender

class IEmcNavigationPortlet(INavigationPortlet):
    
    pass

class Renderer(baseRender):
    
    def createNavTree(self):
        data = self.getNavTree()

        bottomLevel = self.data.bottomLevel or 0

        if bottomLevel < 0:
            # Special case where navigation tree depth is negative
            # meaning that the admin does not want the listing to be displayed
            return self.emcrecurse([], level=1, bottomLevel=bottomLevel)
        else:
            return self.emcrecurse(children=data.get('children', []), level=1, bottomLevel=bottomLevel)
    
    _template = ViewPageTemplateFile('navigation.pt')
    recurse = ViewPageTemplateFile('emc_navigation_recurse.pt')



