#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope.component import getMultiAdapter
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.CMFCore.interfaces import ISiteRoot

from plone.memoize.instance import memoize
from emc.kb import _

from Products.Five.browser import BrowserView

# from collective.gtags.source import TagsSourceBinder
from zope.component import getUtility

# input data view
from plone.directives import form
from z3c.form import field, button
from Products.statusmessages.interfaces import IStatusMessage
from emc.kb.interfaces import InputError
from emc.kb.interfaces import IModelLocator
from emc.kb.mapping_db import Model,IModel
from emc.kb.contents.ormfolder import Iormfolder
# update data view
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from emc.kb import InputDb

from zExceptions import NotFound

grok.templatedir('templates')       

class ModelView(BrowserView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """
              

    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm          
       
        
    def getPathQuery(self):
 
        """返回 all organizations
        """
        query = {}
        query['path'] = "/".join(self.context.getPhysicalPath())
        return query

             
    
    
    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"  
        from emc.kb.mapping_db import  Model
        from emc.kb.interfaces import IModelLocator
        from zope.component import getUtility        
        locator = getUtility(IModelLocator)
#         import pdb
#         pdb.set_trace()
        models = locator.queryModel(start=query['start'],size=query['size'])
        return models

 # ajax multi-condition search relation db      
class ajaxsearch(grok.View):
    """AJAX action for search DB.
    receive front end ajax transform parameters 
    """    
    grok.context(Interface)
    grok.name('dbajaxsearch')
    grok.require('zope2.View')    
#     grok.require('emc.project.view_projectsummary')

    def Datecondition(self,key):        
        "构造日期搜索条件"
        end = datetime.datetime.today()
#最近一周        
        if key == 1:  
            start = end - datetime.timedelta(7) 
#最近一月             
        elif key == 2:
            start = end - datetime.timedelta(30) 
#最近一年            
        elif key == 3:
            start = end - datetime.timedelta(365) 
#最近两年                                                  
        elif key == 4:
            start = end - datetime.timedelta(365*2) 
#最近五年               
        else:
            start = end - datetime.timedelta(365*5) 
#            return    { "query": [start,],"range": "min" }                                                             
        datecondition = { "query": [start, end],"range": "minmax" }
        return datecondition  
          
    def render(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"model_listings")        
 # datadic receive front ajax post data       
        datadic = self.request.form
#         import pdb
#         pdb.set_trace()
        start = int(datadic['start']) # batch search start position
#         datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
#         securitykey = int(datadic['security'])  #密级属性：公开/内部/机密
#         tasktypekey = int(datadic['type']) #任务类型属性：分析/设计/实验/仿真/培训 
#         tag = datadic['tag'].strip()
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()    
#         origquery = searchview.getPathQuery()
        origquery = {}        
        origquery['sort_on'] = sortcolumn 
        # sql db sortt_order:asc,desc 
        origquery['sort_order'] = sortdirection
                
 #模糊搜索       
        if keyword != "":
            origquery['SearchableText'] = '%'+keyword+'%'        
              

#origquery provide  batch search        
        origquery['size'] = size 
        origquery['start'] = start
        
#totalquery  search all 
        totalquery = origquery.copy()
        totalquery['size'] = 0        
        # search all   size = 0 return numbers of recorders                      
        totalnum = searchview.search_multicondition(totalquery)
#         totalnum = len(totalbrains)
        # batch search
        # origquery return batch search result
        # totalquery return all search result         
        resultDicLists = searchview.search_multicondition(origquery)
#        brainnum = len(braindata)         
        del origquery 
        del totalquery
#call output function
# resultDicLists like this:[(u'C7', u'\u4ed6\u7684\u624b\u673a')]       
        data = self.output(start,size,totalnum, resultDicLists)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)       
       
    def output(self,start,size,totalnum,resultDicLists):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""      
        k = 0
        contexturl = self.context.absolute_url()
        for i in resultDicLists:
          
            out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-2 text-left"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="col-md-7">%(description)s</td>                                
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>        
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>        
                                </td>                                                               
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            num=str(k + 1),
                                            title=i[0],
                                            description= i[1],
                                            edit_url="%s/@@update_model/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_model/%s" % (contexturl,i[0]))           
            outhtml = "%s%s" %(outhtml ,out)
            k = k + 1
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data        

class DeleteModel(form.Form):
    "delete the specify model recorder"
    implements(IPublishTraverse)    
    grok.context(Iormfolder)
    grok.name('delete_model')
    grok.require('emc.kb.input_db')
    
    label = _(u"delete model data")
    fields = field.Fields(IModel).omit('modelId','xhdm','xhmc')
    ignoreContext = True
    
    xhdm = None
    #receive url parameters
    def publishTraverse(self, request, name):
        if self.xhdm is None:
            self.xhdm = name
            return self
        else:
            raise NotFound()
    
    def update(self):        
        self.request.set('disable_border', True)
        
        # Get the model table query funcations
        locator = getUtility(IModelLocator)
        #to do 
        #fetch the pending deleting  record 
        self.model = locator.getModelByCode(self.xhdm)       
        #Let z3c.form do its magic
        super(DeleteModel, self).update()

    
    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete model recorder
        """
        
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        
        funcations = getUtility(IModelLocator)
        
        try:
            funcations.DeleteByCode(self.xhdm)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/model_listings')
        
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/model_listings')
    
    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')        
        self.request.response.redirect(self.context.absolute_url() + '/model_listings')    
    

class InputModel(form.Form):
    """input db model table data
    """
    
#     implements(IPublishTraverse)
    
    grok.context(Iormfolder)
    grok.name('input_model')
    grok.require('emc.kb.input_db')
    
    label = _(u"Input model data")
    fields = field.Fields(IModel).omit('modelId')
    ignoreContext = True
 
    
    def update(self):
        
        self.request.set('disable_border', True)
        
        # Get the model table query funcations
#         locator = getUtility(IModelLocator)
        # to do 
        # fetch first record as sample data
#         self.screening = locator.screeningById(self.screeningId)
      
        # Let z3c.form do its magic
        super(InputModel, self).update()

    
    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit model recorder
        """
        
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        
        funcations = getUtility(IModelLocator)
        
        try:
            funcations.addModel(xhdm=data['xhdm'],xhmc=data['xhmc'])
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/model_listings')
        
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/model_listings')
    
    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')        
        self.request.response.redirect(self.context.absolute_url() + '/model_listings')

class UpdateModel(form.Form):
    """update model table row data
    """
    
    implements(IPublishTraverse)    
    grok.context(Iormfolder)
    grok.name('update_model')
    grok.require('emc.kb.input_db')
    
    label = _(u"update model data")
    fields = field.Fields(IModel).omit('modelId','xhdm')
    ignoreContext = True
    
    xhdm = None
    #receive url parameters
    def publishTraverse(self, request, name):
        if self.xhdm is None:
            self.xhdm = name
            return self
        else:
            raise NotFound()
    
    def update(self):        
        self.request.set('disable_border', True)
        
        # Get the model table query funcations
#         locator = getUtility(IModelLocator)
        # to do 
        # fetch first record as sample data
#         self.screening = locator.screeningById(self.screeningId)
       
        # Let z3c.form do its magic
        super(UpdateModel, self).update()

    
    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update model recorder
        """
        
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        
        funcations = getUtility(IModelLocator)
#         import pdb
#         pdb.set_trace()
        
        try:
            funcations.updateByCode(xhdm=self.xhdm,xhmc=data['xhmc'])
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/model_listings')
        
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/model_listings')
    
    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')        
        self.request.response.redirect(self.context.absolute_url() + '/model_listings')
