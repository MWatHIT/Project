import imp
import os

from plone.uuid.interfaces import IUUID
import zope.component.interfaces
from zope.interface import implements
from zope.component.interfaces import ObjectEvent
class IPyfileAddedEvent(zope.component.interfaces.IObjectEvent):
    """
    send the event after a previewable file has been created 
    """
class PyfileAddedEvent(ObjectEvent):
    """An python file  has been created"""

    implements(IPyfileAddedEvent)
    
def load_from_file(filepath):
#     class_inst = None
#     expected_class = 'FileView'
    mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

#     if hasattr(py_mod, expected_class):
#         class_inst = getattr(py_mod, expected_class)()

    return py_mod

def tmp_file_name(uid,ext="py"):
        "generate tmp file for py file and output html file"
#         predir = "~/tmp"
#         dir = os.path.expanduser(predir)
        dir = "/home/plone/tmp" 
#         temp = os.tempnam(dir)
        tmp_py = "%s/%s.%s" % (dir,uid,ext)
        tmp_html = "%s/%s.%s" % (dir,uid,'html')
        return tmp_py,tmp_html
    
def pyfile_subscriber_handler(obj,event):
    "when py file created or modified ,fire up the event,the handler process relative actions"
    "1 create or update the py file's temp file in file system"
    "2 create or update bokeh html output file"
#     from bokeh.io import output_file
#     from bokeh.io import show
    
 
#     import pdb
#     pdb.set_trace()
    uid = IUUID(obj,None)
    py,html = tmp_file_name(uid)
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
    return None
    
#     output_file(html)
#     bokeh = load_from_file(py)
#     show(bokeh.p)
           