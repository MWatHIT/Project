#-*- coding: UTF-8 -*-
import sqlalchemy.types
import sqlalchemy.schema
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from five import grok
from zope import schema
from zope.interface import Interface,implements
from emc.kb import ORMBase
from emc.kb import _

class IModel(Interface):
    """编号number 记录表
    """
    modelId = schema.Int(
            title=_(u"model table primary key"),
        )   
    # 型号代码
    xhdm = schema.TextLine(
            title=_(u"model code"),
        )    
    #型号名称
    xhmc = schema.TextLine(
            title=_(u"model name"),
        )

class Model(ORMBase):
    """Database-backed implementation of IModel
    """
    implements(IModel)
    
    __tablename__ = 'model'
    
    modelId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
        
    xhdm = sqlalchemy.schema.Column(sqlalchemy.types.String(8),
            nullable=False,
        )
    xhmc = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )

class Modeltest(ORMBase):
    """Database-backed implementation of IModel
    """
#     implements(IModel)
    
    __tablename__ = 'modeltest2'
    
    ID = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
                                       primary_key=True,)
    XHDM = sqlalchemy.schema.Column(sqlalchemy.types.String(8))
    XHMC = sqlalchemy.schema.Column(sqlalchemy.types.String(32))    

class IBranch(Interface):
    """分系统表 branch
    """
    branchId = schema.Int(
            title=_(u"branch table primary key"),
        )
    model = schema.Object(
            title=_(u"Model record"),
            schema=IModel,
        )      
    modelId = schema.Int(
            title=_(u"branch table foreign key"),
        )       
    # 分系统代码
    fxtdm = schema.TextLine(
            title=_(u"branch code"),
        )    
    #分系统名称
    fxtmc = schema.TextLine(
            title=_(u"branch name"),
        )
    #分系统类别
    fxtlb = schema.TextLine(
            title=_(u"branch category"),
        )
class Branch(ORMBase):
    """Database-backed implementation of IBranch
    """
    implements(IBranch)
    
    __tablename__ = 'branch'
    
    branchId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
   
    modelId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            sqlalchemy.schema.ForeignKey('model.modelId'),
            nullable=False,
        )
    model = relationship("Model", backref=backref('branches', order_by=branchId))
#     model = sqlalchemy.orm.relation(Model,primaryjoin=Model.modelId==modelId,)             
    fxtdm = sqlalchemy.schema.Column(sqlalchemy.types.String(16),
            nullable=False,
        )
    fxtmc = sqlalchemy.schema.Column(sqlalchemy.types.String(64),
            nullable=False,
        ) 
    fxtlb = sqlalchemy.schema.Column(sqlalchemy.types.String(16),
            nullable=False,
        )        

