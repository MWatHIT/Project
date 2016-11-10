#-*- coding: UTF-8 -*-
from five import grok
from zope import schema
from zope.interface import Interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
import datetime

from z3c.form.form import extends
from z3c.form import field

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.directives import form, dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.namedfile.field import NamedBlobFile

from collective import dexteritytextindexer

from plone.app.contenttypes.interfaces import IFile

#from collective.dexteritytextindexer.behavior import IDexterityTextIndexer
from emc.bokeh.browser.interfaces import BokehNamedFileFieldWidget
from emc.bokeh import _



#图像数据schema,包括x坐标，y坐标
class IPlotDataSchema(Interface):
    x = schema.Float(title=_(u"X Coordinate"))
    y = schema.Float(title=_(u"Y Coordinate"))


class IFearture(form.Schema,IBasic):
    """
    emc project features content type
    """
#标准名称
    dexteritytextindexer.searchable('title')    
    title = schema.TextLine(title=_(u"standard name"),
                             default=u"",
                            required=True,) 
#标准描述        
    description = schema.TextLine(title=_(u"standard description"),
                             default=u"",
                             required=False,)
#图例       
    legend = schema.TextLine(title=_(u"a legend of the  first figure"),
                             default=u"",
                             required=True,)
#图例       
    legend2 = schema.TextLine(title=_(u"a legend of the second figure"),
                             default=u"",
                             required=False,)    
#坐标类型
    x_axis_type = schema.Choice(
        title=_(u"x axis type"),     
        vocabulary="emc.bokeh.vocabulary.axistype",
        default="linear",   
        required=True
    )  
    y_axis_type = schema.Choice(
        title=_(u"y axis type?"),     
        vocabulary="emc.bokeh.vocabulary.axistype",
        default="linear",   
        required=True
    )        
# 坐标名称：
    x_axis_label = schema.TextLine(
        title=_(u"x axis label"),    
        default=u"X",   
        required=False
    )  
    y_axis_label = schema.TextLine(
        title=_(u"y axis label"),     
        default=u"Y",   
        required=False
    )           

#数据来源 
    source = schema.Choice(
        title=_(u"Where the source data that will composing the plot come from ?"),     
        vocabulary="emc.bokeh.vocabulary.sourcetype",
        default="inline",   
        required=True
    )
    source2 = schema.Choice(
        title=_(u"Where the source data that will composing the plot come from ?"),     
        vocabulary="emc.bokeh.vocabulary.sourcetype",
        default="inline",   
        required=False
    )


# 图像数据字段 在线输入
    form.widget(coordination=DataGridFieldFactory)
    coordination = schema.List(title=_(u"coordination data"),
        value_type=DictRow(title=_(u"coordination data row"), schema=IPlotDataSchema),
        required=False,
        )
# 图像数据字段 在线输入
    form.widget(coordination2=DataGridFieldFactory)
    coordination2 = schema.List(title=_(u"coordination data"),
        value_type=DictRow(title=_(u"coordination data row"), schema=IPlotDataSchema),
        required=False,
        )
#包含图像数据的csv文件   
    form.widget(upload=BokehNamedFileFieldWidget)
    upload = NamedBlobFile(title=_(u"figure data"),
        description=_(u"Attach your figure data report file(csv format)."),
        required=False,
    )
#包含图像数据的csv文件   
    form.widget(upload2=BokehNamedFileFieldWidget)
    upload2 = NamedBlobFile(title=_(u"the second figure data"),
        description=_(u"Attach your figure data report file(csv format)."),
        required=False,
    )    
# 知识库中引用
    reference = RelationChoice(
        title=_(u"reference"),
        source=ObjPathSourceBinder(object_provides=IFile.__identifier__),
        required=False,
    )
# 知识库中引用,file should be csv
    reference2 = RelationChoice(
        title=_(u"reference"),
        source=ObjPathSourceBinder(object_provides=IFile.__identifier__),
        required=False,
    )    
# 字段集        
    form.fieldset('secondsource',
            label=_(u"second chart"),
            fields=['legend2','source2','coordination2','upload2','reference2']
    )    
class EditForm(form.EditForm):
    extends(form.EditForm)

    grok.context(IFearture)
    grok.require('zope2.View')
    fields = field.Fields(IFearture)
    label=_(u"modify standard parameters for Plotting the figure")

    fields['coordination'].widgetFactory = DataGridFieldFactory


         