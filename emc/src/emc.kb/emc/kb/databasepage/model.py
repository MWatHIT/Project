#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements

#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func

from emc.kb import kb_session
from emc.kb.mapping_db import Model
from emc.kb.interfaces import IModelLocator

from emc.kb import  _

# set sqlarchemy db sources
# from z3c.saconfig.utility import EngineFactory
# from z3c.saconfig.utility import GloballyScopedSession
# from zope.component.hooks import getSite
# from collective.saconnect.interfaces import ISQLAlchemyConnectionStrings
# from zope.component import provideUtility,queryUtility

class ModelLocator(grok.GlobalUtility):
    implements(IModelLocator)
    
    def addModel(self,**kwargs):
        """parameters db model table"""
        model = Model()
#         model.modelId = kwargs['modelId']
        model.xhdm = kwargs['xhdm']
        model.xhmc = kwargs['xhmc']
# # registry db sources
#         import pdb
#         pdb.set_trace()
# 
#         saconnect = ISQLAlchemyConnectionStrings(getSite())
# # Register z3c.saconfig utilities for mysql parameters db
#         dbURI = saconnect['mysql']
# # Register z3c.saconfig utilities for pas.plugins.sqlarchemy
#         engine = EngineFactory(dbURI, echo=False, convert_unicode=False)
#         provideUtility(engine, name=u"mysql.parameters")        
#         session = GloballyScopedSession(engine=u"mysql.parameters", twophase=False)
#         provideUtility(session,name=u"mysql.parameters") 
        kb_session.add(model)
        try:
            kb_session.commit()
        except:
            kb_session.rollback()
            pass
        
    def queryModel(self,**kwargs):
        """以分页方式提取model 记录，参数：start 游标起始位置；size:每次返回的记录条数;
        fields:field list
        if size = 0,then不分页，返回所有记录集
        order_by(text("id"))
        """    
                            
        start = int(kwargs['start'])
        size = int(kwargs['size'])
#         fields = kwargs['fields']
        if size != 0:
            models = kb_session.query("xhdm", "xhmc").\
            from_statement(
            text("select * from model  order by modelId desc limit :start,:size").\
            params(start=start,size=size)).all()            
        else:
#             import pdb
#             pdb.set_trace()
            nums = kb_session.query(func.count(Model.modelId)).scalar()
#             nums = kb_session.query("xhdm", "xhmc").from_statement(text("select * from model")).count()
            return int(nums) 
        try:

            kb_session.commit()            
            return models  
        except:
            kb_session.rollback()
            pass
    
    def DeleteByCode(self,xhdm):
        "delete the specify xhdm model recorder"

#         xhdm = kwargs['xhdm']
        if xhdm != "":
            try:
                model = kb_session.query(Model).\
                from_statement(text("SELECT * FROM model where xhdm=:xhdm")).\
                params(xhdm=xhdm).one()
                kb_session.delete(model)                                                  
                kb_session.commit()           
            except:
                kb_session.rollback()
                pass
        else:
            return None
    
    def updateByCode(self,**kwargs):
        "update the speicy xhdm model recorder"
        
        """
        session.query(User).from_statement(text("SELECT * FROM users where name=:name")).\
params(name='ed').all()
session.query(User).from_statement(
text("SELECT * FROM users where name=:name")).params(name='ed').all()
        """

        xhdm = kwargs['xhdm']
#         import pdb
#         pdb.set_trace()
        if xhdm != "":
            try:
                model = kb_session.query(Model).\
                from_statement(text("SELECT * FROM model where xhdm=:xhdm")).\
                params(xhdm=xhdm).one()
#                 for kw in kwargs.keys():
#                     model.kw = kwargs[kw]                                                     
                model.xhmc = kwargs['xhmc']
                kb_session.commit()           
            except:
                kb_session.rollback()
                pass
        else:
            return None

    def getModelByCode(self,xhdm):

#         xhdm = kwargs['xhdm']
        if xhdm != "":
            try:
                model = kb_session.query(Model).\
                from_statement(text("SELECT * FROM model where xhdm=:xhdm")).\
                params(xhdm=xhdm).one()
                return model          
            except:
                kb_session.rollback()
                None
        else:
            return None
                                