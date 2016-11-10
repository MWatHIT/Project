#-*- coding: UTF-8 -*-
# from five import grok
import json
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot
from emc.policy import _
from emc.project.content.project import IProject
from emc.project.content.projectfolder import IProjectFolder

from emc.theme.interfaces import IThemeSpecific
from emc.project.browser.ajax_listing import sysAjaxListingView,ajaxsearch
# from emc.memberArea.browser.workspace import WorkspaceView
from emc.kb.contents.kbfolder import Ikbfolder


# grok.templatedir('templates')

class FrontpageView(sysAjaxListingView):
     
#     grok.context(ISiteRoot)
#     grok.template('ajax_listings_homepage')
#     grok.name('index.html')
#     grok.layer(IThemeSpecific)
#     grok.require('zope2.View')      
       
    def getPathQuery(self):
 
        """返回 知识库目录
        """
        query = {}
        kb = self.getKBFolder()

        query['path'] = "/".join(kb.getPhysicalPath())
        return query         
        
# roll table output
    def getKBFolder(self):
        
        brains = self.catalog()({'object_provides':Ikbfolder.__identifier__})
        context = brains[0].getObject()
        return context        
        
class search(ajaxsearch):
    
    
    def render(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"index.html")        
 # datadic receive front ajax post data       
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
#         securitykey = int(datadic['security'])  #密级属性：公开/内部/机密
#         tasktypekey = int(datadic['type']) #任务类型属性：分析/设计/实验/仿真/培训 
        tag = datadic['tag'].strip()
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = searchview.getPathQuery()
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
                
 #模糊搜索       
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

#         if securitykey != 0:
#             origquery['security_level'] = searchview.getSecurityLevel(securitykey)
        if datekey != 0:
            origquery['created'] = self.Datecondition(datekey)           
#         if tasktypekey != 0:
#             origquery['task_type'] = searchview.getTaskType(tasktypekey)

        # remove repeat values 
        tag = tag.split(',')
        tag = set(tag)
        tag = list(tag)
        all = u"所有".encode("utf-8")
        unclass = u"未分类".encode("utf-8")        
# filter contain "u'所有'"
        tag = filter(lambda x: all not in x, tag)
# recover un-category tag (remove:u"未分类-")
        def recovery(value):
            if unclass not in value:return value
            return value.split('-')[1]
            
        tag = map(recovery,tag)        
        if '0' in tag and len(tag) > 1:
            tag.remove('0')
            rule = {"query":tag,"operator":"and"}
            origquery['Subject'] = rule
                      
#totalquery  search all 
        totalquery = origquery.copy()
#origquery provide  batch search        
        origquery['b_size'] = size 
        origquery['b_start'] = start
        # search all                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)
        # batch search         
        braindata = searchview.search_multicondition(origquery)
#        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains
#call output function        
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)     
            
