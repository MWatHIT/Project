# -*- coding: utf-8 -*-
#
# File: ARFilePreview/events.py
#
# Copyright (c) 2007 atReal
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

"""
$Id$
"""

__author__ = """Jean-Nicolas Bès <contact@atreal.net>"""
__docformat__ = 'plaintext'
__licence__ = 'GPL'


from zope.interface import implements
from zope.component.interfaces import ObjectEvent
from collective.filepreviewbehavior.interfaces import IPreviewable
from collective.filepreviewbehavior.interfaces import IPreviewableFileCreatedEvent

class PreviewableFileCreatedEvent(ObjectEvent):
    """An previewable file  has been created"""

    implements(IPreviewableFileCreatedEvent)

# @grok.subscribe(IPreviewable,IObjectAddedEvent)
def buildAndStorePreview(obj, event):
    """ """
    if hasattr(obj,'buildPreview'):
        if not obj.buildPreview:
            print "buildPreview == False, we don't have to build the preview"
            return
    print "BUILD AND STORE PREVIEW %s" % ( obj.getPhysicalPath() , )
    IPreviewable(obj).buildAndStorePreview()

def UpdateFileInfo(obj, event):
    """ """
    print "Update file information %s" % ( obj.getPhysicalPath() , )
    IPreviewable(obj).UpdateFileInfo()    

        
