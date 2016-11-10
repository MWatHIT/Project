#-*- coding:utf-8 -*-
from types import ClassType, FileType, StringType, UnicodeType
from webdav.common import rfc1123_date
from plone.app.blob.download import handleIfModifiedSince, handleRequestRange
from Products.Archetypes.utils import contentDispositionHeader
# 解决下载时不显示中文名称bug
def index_html(self, REQUEST=None, RESPONSE=None, charset='utf-8', disposition='inline'):
        """ make it directly viewable when entering the objects URL """

        if REQUEST is None:
            REQUEST = self.REQUEST

        if RESPONSE is None:
            RESPONSE = REQUEST.RESPONSE

        RESPONSE.setHeader('Last-Modified', rfc1123_date(self._p_mtime))
        RESPONSE.setHeader('Content-Type', self.getContentType())
        RESPONSE.setHeader('Accept-Ranges', 'bytes')

        if handleIfModifiedSince(self, REQUEST, RESPONSE):
            return ''

        length = self.get_size()
        RESPONSE.setHeader('Content-Length', length)

        filename = self.getFilename()
        if filename is not None:
            if REQUEST.HTTP_USER_AGENT.find('MSIE') != -1:
                if isinstance(filename,unicode):
                    filename = filename.encode('gb18030')
                else:
                    filename = unicode(filename,charset,errors="ignore")
                    filename = filename.encode('gb18030')
                header_value = contentDispositionHeader(disposition, 'gb18030', filename=filename)
            else:
                if not isinstance(filename, unicode):                
                    filename = unicode(filename, charset, errors="ignore")

                    
                        
#            filename = IUserPreferredFileNameNormalizer(REQUEST).normalize(
#                filename)
                header_value = contentDispositionHeader(
                disposition=disposition,
                filename=filename)
            RESPONSE.setHeader("Content-disposition", header_value)

        request_range = handleRequestRange(self, length, REQUEST, RESPONSE)
        return self.getIterator(**request_range)      

