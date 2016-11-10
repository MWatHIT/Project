from cgi import escape
from datetime import date
from urllib import unquote

from plone.registry.interfaces import IRegistry

from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.component import getUtility
from zope.deprecation.deprecation import deprecate
from zope.i18n import translate
from zope.interface import implements, alsoProvides
from zope.viewlet.interfaces import IViewlet

from AccessControl import getSecurityManager
from Acquisition import aq_base, aq_inner

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ISiteSchema
from Products.CMFPlone.interfaces import ISearchSchema
from Products.CMFPlone.utils import safe_unicode, getSiteLogo
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.common import LogoViewlet as base
from plone.app.layout.viewlets.common import ViewletBase
from plone.protect.utils import addTokenToUrl

class SearchBoxViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/searchbox.pt')

    def update(self):
        super(SearchBoxViewlet, self).update()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')

        registry = getUtility(IRegistry)
        search_settings = registry.forInterface(ISearchSchema, prefix='plone')
        self.livesearch = search_settings.enable_livesearch

        folder = context_state.folder()
        self.folder_path = '/'.join(folder.getPhysicalPath())

    @memoize
    def data_pat_livesearch(self):
        navroot = self.navigation_root_url
        out = "ajaxUrl:%s/@@ajax-search;minimumInputLength:2" % navroot
        return out

class LogoViewlet(base):
    index = ViewPageTemplateFile('templates/logo.pt')

    def update(self):
        super(LogoViewlet, self).update()

        # TODO: should this be changed to settings.site_title?
        self.navigation_root_title = self.portal_state.navigation_root_title()

        site_url = self.portal_state.portal_url()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSchema,
                                         prefix="plone",
                                         check=False)
        self.logo_title = settings.site_title
        self.img_src = "%s/++resource++emc.policy/images/logo.png" % site_url
#         self.img_src = getSiteLogo(self.portal_state.portal())


# class GlobalSectionsViewlet(ViewletBase):
#     index = ViewPageTemplateFile('sections.pt')
# 
#     def update(self):
#         context = aq_inner(self.context)
#         portal_tabs_view = getMultiAdapter((context, self.request),
#                                            name='portal_tabs_view')
#         self.portal_tabs = portal_tabs_view.topLevelTabs()
# 
#         self.selected_tabs = self.selectedTabs(portal_tabs=self.portal_tabs)
#         self.selected_portal_tab = self.selected_tabs['portal']
# 
#     def selectedTabs(self, default_tab='index_html', portal_tabs=()):
#         plone_url = getToolByName(self.context, 'portal_url')()
#         plone_url_len = len(plone_url)
#         request = self.request
#         valid_actions = []
# 
#         url = request['URL']
#         path = url[plone_url_len:]
#         path_list = path.split('/')
#         if len(path_list) <= 1:
#             return {'portal': default_tab}
# 
#         for action in portal_tabs:
#             if not action['url'].startswith(plone_url):
#                 # In this case the action url is an external link. Then, we
#                 # avoid issues (bad portal_tab selection) continuing with next
#                 # action.
#                 continue
#             action_path = action['url'][plone_url_len:]
#             if not action_path.startswith('/'):
#                 action_path = '/' + action_path
#             action_path_list = action_path.split('/')
#             if action_path_list[1] == path_list[1]:
#                 # Make a list of the action ids, along with the path length
#                 # for choosing the longest (most relevant) path.
#                 valid_actions.append((len(action_path_list), action['id']))
# 
#         # Sort by path length, the longest matching path wins
#         valid_actions.sort()
#         if valid_actions:
#             return {'portal': valid_actions[-1][1]}
# 
#         return {'portal': default_tab}

class PathBarViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/path_bar.pt')

    def update(self):
        super(PathBarViewlet, self).update()

        self.is_rtl = self.portal_state.is_rtl()

        breadcrumbs_view = getMultiAdapter((self.context, self.request),
                                           name='breadcrumbs_view')
        self.breadcrumbs = breadcrumbs_view.breadcrumbs()
