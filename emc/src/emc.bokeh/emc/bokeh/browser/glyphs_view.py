#-*- coding: UTF-8 -*-
from five import grok
from z3c.form import field
from plone.directives import dexterity
from plone.memoize.instance import memoize
from emc.bokeh.content.glyphs import IFearture
import csv
from StringIO import StringIO

from emc.bokeh import _

grok.templatedir('templates') 

# need byte string
data_VALUES = [
               u"x坐标".encode('utf-8'),
               u"y坐标".encode('utf-8'),
               ]

class FeartureView(grok.View):
    "emc fearture view"
    grok.context(IFearture)
    grok.template('fearture_view')
    grok.name('view')
    grok.require('zope2.View')    
    


    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm    
            
    @property
    def isEditable(self):
        return self.pm().checkPermission(permissions.ManagePortal,self.context) 

    def _createCSV(self, lines):
        """Write header and lines within the CSV file."""
        datafile = StringIO()
        writor = csv.writer(datafile)
        writor.writerow(data_VALUES)
        map(writor.writerow, lines)
        return datafile

    def _createRequest(self, data, filename):
        """Create the request to be returned.

        Add the right header and the CSV file.
        """
        self.request.response.addHeader('Content-Disposition', "attachment; filename=%s" % filename)
        self.request.response.addHeader('Content-Type', "text/csv;charset=utf-8")
        self.request.response.addHeader("Content-Transfer-Encoding", "8bit")        
        self.request.response.addHeader('Content-Length', "%d" % len(data))
        self.request.response.addHeader('Pragma', "no-cache")
        self.request.response.addHeader('Cache-Control', "must-revalidate, post-check=0, pre-check=0, public")
        self.request.response.addHeader('Expires', "0")
        return data 

    def getCSVTemplate(self):
        """Return a CSV template to use when upload figure data."""
        datafile = self._createCSV([])
        return self._createRequest(datafile.getvalue(), "orgs_sheet_template.csv")     

        
 # fetch data
    def getData(self,source="upload",datadic=None,upload=None,reference=None):
#         source = self.context.source
        data={'x':[],'y':[]}
        if source == 'inline':        
           # this is a list,and every item of the list must be dic
#            datadic = self.context.coordination
           if datadic == None:return None
           for d in datadic:
                m = d['x']
                n = d['y']
                if m ==None:
                    data['x'].append(0)
                else:
                    data['x'].append(m)
                if n == None:
                    data['y'].append(0)
                else:
                    data['y'].append(n)           

           return data
        elif source =='upload':
#             fo = self.context.upload
            reader = upload.data
            #split byte string to get all rows
            rows = reader.split('\n')
            #the first row is header cell,it must be same with template file's the first row.
            header = rows[0].split(',')
            if header != data_VALUES:
                msg = _('Wrong specification of the CSV file. Please correct it and retry.')
                type = 'error'
                IStatusMessage(self.request).addStatusMessage(msg, type=type)
                return  None
            else:
                # data row
                for row in rows[1:]:
                    line = row.split(',')
                    #remove space line
                    if len(line) ==2:
                        data['x'].append(float(line[0]))
                        data['y'].append(float(line[1]))
                    else:
                        continue
                return data                              
# KB reference
        else:
#            rel = self.context.reference
           ob = reference.to_object
           reader = ob.file.data
           rows = reader.split('\n')

            #the first row is header cell,it must be same with template file's the first row.
           header = rows[0].split(',')
           if header != data_VALUES:
                msg = _('Wrong specification of the CSV file. Please correct it and retry.')
                type = 'error'
                IStatusMessage(self.request).addStatusMessage(msg, type=type)
                return  None
           else:
                # data row
                for row in rows[1:]:
                    line = row.split(',')
                    #remove space line
                    if len(line) ==2:
                        data['x'].append(float(line[0]))
                        data['y'].append(float(line[1]))
                    else:
                        continue
                return data           

    @memoize         
    def getPlot(self):
        """using bokeh output glyphs
        """
        from bokeh.plotting import figure
        from bokeh.embed import components
        source = self.context.source
        #online input data
        datadic = self.context.coordination
        #data file upload
        upload = self.context.upload
        # klnowlege db refer
        rel = self.context.reference
        data = self.getData(source=source,datadic=datadic,upload=upload,reference=rel)
        #if no any data,using dummy data 
        if data ==None:
            x = [1, 2, 3, 4, 5]
            y = [6, 7, 2, 4, 5]
        else:
            x = data['x']
            y = data['y']

        # create a new plot with a title and axis labels
        p = figure(title=self.context.title,
                   x_axis_label=self.context.x_axis_label,
                   y_axis_label=self.context.y_axis_label,
                   y_axis_type=self.context.y_axis_type,
                   x_axis_type=self.context.x_axis_type)      
        # add a line renderer with legend and line thickness
        p.line(x, y, legend=self.context.legend, line_color="red",line_width=2)
        #draw the second line.        
        source = self.context.source2
        #online input data
        datadic = self.context.coordination2
        #data file upload
        upload = self.context.upload2
        # klnowlege db refer
        rel = self.context.reference2
        data = self.getData(source=source,datadic=datadic,upload=upload,reference=rel)

        #if no any data,skip
        if data != None:
            x = data['x']
            y = data['y']            
            p.line(x, y, legend=self.context.legend2, line_color="blue",line_width=2)                             
        script, div = components(p)
        out = {}
        out['js'] = script
        out['div'] = div
        return out    
        
