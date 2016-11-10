#-*- coding: UTF-8 -*-
import csv
from StringIO import StringIO
from zope import event
from zope.interface import implements

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


data_PROPERTIES = [
    'title',
    'description',
    'address',
    'legal_person',        
    'supervisor',
    'register_code',
    'belondto_area',
    'organization_type',
    'announcement_type',
    'passDate'
    ] 
# need byte string
data_VALUES = [
               u"x坐标".encode('utf-8'),
               u"y坐标".encode('utf-8'),
               ]


class DataInOut (BrowserView):
    """Data import and export as CSV files.
    """

    def __call__(self):
        method = self.request.get('REQUEST_METHOD', 'GET')
        if (method != 'POST') or not int(self.request.form.get('form.submitted', 0)):
            return self.index()

        if self.request.form.get('form.button.Cancel'):
            return self.request.response.redirect('%s/plone_control_panel' \
                                                  % self.context.absolute_url())



        

    def getCSVTemplate(self):
        """Return a CSV template to use when importing members."""
        datafile = self._createCSV([])
        return self._createRequest(datafile.getvalue(), "data_template.csv")     


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
