#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema

from emc.kb import _
    
class InputError(Exception):
    """Exception raised if there is an error making a data input
    """

# db insterface
class IModelLocator (Interface):
    """medel table add row"""
    
    def addModel(self):
        "add a model data"
        
    def queryModel(self):
        "query model by search condition"
        
class IBranchLocator (Interface):
    """medel table add row"""
    
    def addBranch(self):
        "add a model data"
        
    def queryBranch(self):
        "query model by search condition"             
    