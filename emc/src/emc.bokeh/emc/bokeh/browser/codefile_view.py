#-*- coding: UTF-8 -*-
import os
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone.memoize.instance import memoize
from plone.uuid.interfaces import IUUID

from emc.bokeh.utils import tmp_file_name,load_from_file
from emc.bokeh import _



class CodeFileView(BrowserView):
    "emc fearture view"
             
    
    def create_tmp_file(self,obj,py):
        "create tmp py file"
        
        try:
            body = obj.manage_FTPget()
        except:
            return None

        bad = ["exec","open"]
        body_f = open(py, 'wb')
        for data in body:
            if bad[0] not in data and bad[1] not in data:            
                body_f.write(data)
            else:
                continue
        body_f.close()
    
    @memoize            
    def getPlot(self):
        """using bokeh output glyphs
        """
        from bokeh.embed import components
#         import pdb
#         pdb.set_trace()
        context = aq_inner(self.context)
        uid = IUUID(context,None)
        py,html = tmp_file_name(uid)
        # druge py file is exist?
        if os.path.isfile(py):
            pass
        else:            
        # create
            self.create_tmp_file(context,py)       

        try:
            bokeh = load_from_file(py)
        except:
            return {"js":"","div":"<div class='text-error'>the uploaded python file has syntax errors!</div>"}
        script, div = components(bokeh.p)
        out = {}
        out['js'] = script
        out['div'] = div
        return out         
        
  
        
