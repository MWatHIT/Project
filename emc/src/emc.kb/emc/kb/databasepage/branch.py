#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements

#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func

from emc.kb import kb_session
from emc.kb.mapping_db import Branch
from emc.kb.interfaces import IBranchLocator

from emc.kb import  _

class BranchLocator(grok.GlobalUtility):
    implements(IBranchLocator)
    
    def add(self,argsdic):
        """parameters db branch table"""
        branch = Branch()
        for kw in argsdic.keys():
            setattrib(branch,kw,argsdic[kw])

        kb_session.add(branch)
        try:
            kb_session.commit()
        except:
            kb_session.rollback()
            pass
        
    def query(self,**kwargs):
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
            text("select * from branch  order by branchId desc limit :start,:size").\
            params(start=start,size=size)).all()            
        else:
#             import pdb
#             pdb.set_trace()
            nums = kb_session.query(func.count(Branch.branchId)).scalar()
#             nums = kb_session.query("xhdm", "xhmc").from_statement(text("select * from branch")).count()
            return int(nums) 
        try:

            kb_session.commit()            
            return models  
        except:
            kb_session.rollback()
            pass
    
    def DeleteByCode(self,xhdm):
        "delete the specify xhdm branch recorder"

#         xhdm = kwargs['xhdm']
        if xhdm != "":
            try:
                branch = kb_session.query(Branch).\
                from_statement(text("SELECT * FROM branch where xhdm=:xhdm")).\
                params(xhdm=xhdm).one()
                kb_session.delete(branch)                                                  
                kb_session.commit()           
            except:
                kb_session.rollback()
                pass
        else:
            return None
    
    def updateByCode(self,**kwargs):
        "update the speicy xhdm branch recorder"
        
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
                branch = kb_session.query(Branch).\
                from_statement(text("SELECT * FROM branch where xhdm=:xhdm")).\
                params(xhdm=xhdm).one()
#                 for kw in kwargs.keys():
#                     branch.kw = kwargs[kw]                                                     
                branch.xhmc = kwargs['xhmc']
                kb_session.commit()           
            except:
                kb_session.rollback()
                pass
        else:
            return None

    def getByCode(self,xhdm):

#         xhdm = kwargs['xhdm']
        if xhdm != "":
            try:
                branch = kb_session.query(Branch).\
                from_statement(text("SELECT * FROM branch where xhdm=:xhdm")).\
                params(xhdm=xhdm).one()
                return branch          
            except:
                kb_session.rollback()
                None
        else:
            return None
                                