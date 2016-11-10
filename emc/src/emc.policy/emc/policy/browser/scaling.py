from Acquisition import aq_base
from AccessControl.ZopeGuards import guarded_getattr
from DateTime import DateTime
from logging import exception
from plone.namedfile.interfaces import IAvailableSizes
from plone.namedfile.interfaces import IStableImageScale
from plone.namedfile.utils import set_headers, stream_data
from plone.rfc822.interfaces import IPrimaryFieldInfo
from plone.scale.storage import AnnotationStorage
from plone.scale.scale import scaleImage
from Products.Five import BrowserView
from xml.sax.saxutils import quoteattr
from ZODB.POSException import ConflictError
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.interface import implements
from zope.traversing.interfaces import ITraversable, TraversalError
from zope.publisher.interfaces import IPublishTraverse, NotFound
from zope.app.file.file import FileChunk
from plone.protect.interfaces import IDisableCSRFProtection

_marker = object()

from plone.namedfile.scaling import ImageScaling,ImageScale,ImmutableTraverser



class ImageScaling(ImageScaling):
    """ view used for generating (and storing) image scales """
    implements(ITraversable, IPublishTraverse)
    # Ignore some stacks to help with accessing via webdav, otherwise you get a
    # 404 NotFound error.
    _ignored_stacks = ('manage_DAVget', 'manage_FTPget')

    def publishTraverse(self, request, name):
        """ used for traversal via publisher, i.e. when using as a url """
        stack = request.get('TraversalRequestNameStack')
        image = None
        if stack and stack[-1] not in self._ignored_stacks:
            # field and scale name were given...
            scale = stack.pop()
            image = self.scale(name, scale)             # this is aq-wrapped
        elif '-' in name:
            # we got a uid...
            if '.' in name:
                name, ext = name.rsplit('.', 1)
            storage = AnnotationStorage(self.context)
            info = storage.get(name)
            if info is not None:
                scale_view = ImageScale(self.context, self.request, **info)
                alsoProvides(scale_view, IStableImageScale)
                return scale_view.__of__(self.context)
        else:
            # otherwise `name` must refer to a field...
            if '.' in name:
                name, ext = name.rsplit('.', 1)
            value = getattr(self.context, name)
            scale_view = ImageScale(
                self.context, self.request, data=value, fieldname=name)
            return scale_view.__of__(self.context)
        if image is not None:
            return image
        raise NotFound(self, name, self.request)

    def traverse(self, name, furtherPath):
        """ used for path traversal, i.e. in zope page templates """
        # validate access
        value = self.guarded_orig_image(name)
        if not furtherPath:
            image = ImageScale(
                self.context, self.request, data=value, fieldname=name)
        else:
            return ImmutableTraverser(self.scale(name, furtherPath[-1]))

        if image is not None:
            return image.tag()
        raise TraversalError(self, name)

    _sizes = {}

    def getAvailableSizes(self, fieldname=None):
        # fieldname is ignored by default
        getAvailableSizes = queryUtility(IAvailableSizes)
        if getAvailableSizes is None:
            return self._sizes
        sizes = getAvailableSizes()
        if sizes is None:
            return {}
        return sizes

    def _set_sizes(self, value):
        self._sizes = value

    available_sizes = property(getAvailableSizes, _set_sizes)

    def getImageSize(self, fieldname=None):
        if fieldname is not None:
            value = self.guarded_orig_image(fieldname)
            if value is None:
                return (0, 0)
            return value.getImageSize()
        value = IPrimaryFieldInfo(self.context).value
        return value.getImageSize()

    def guarded_orig_image(self, fieldname):
        return guarded_getattr(self.context, fieldname, None)

    def getQuality(self):
        """Get plone.app.imaging's quality setting"""
        # Avoid dependening on version where interface first
        # appeared.
        try:
            from plone.scale.interfaces import IScaledImageQuality
        except ImportError:
            return None
        getScaledImageQuality = queryUtility(IScaledImageQuality)
        if getScaledImageQuality is None:
            return None
        return getScaledImageQuality()

    def create(self,
               fieldname,
               direction='thumbnail',
               height=None,
               width=None,
               **parameters):
#         import pdb
#         pdb.set_trace()        
        """ factory for image scales, see `IImageScaleStorage.scale` """
        orig_value = getattr(self.context, fieldname)
        if orig_value is None:
            return

        if height is None and width is None:
            _, format = orig_value.contentType.split('/', 1)
            return None, format, (orig_value._width, orig_value._height)
        if hasattr(aq_base(orig_value), 'open'):
            orig_data = orig_value.open()
        else:
            orig_data = getattr(aq_base(orig_value), 'data', orig_value)
        if not orig_data:
            return

        # Handle cases where large image data is stored in FileChunks instead
        # of plain string
        if isinstance(orig_data, FileChunk):
            # Convert data to 8-bit string
            # (FileChunk does not provide read() access)
            orig_data = str(orig_data)

        # If quality wasn't in the parameters, try the site's default scaling
        # quality if it exists.
        if 'quality' not in parameters:
            quality = self.getQuality()
            if quality:
                parameters['quality'] = quality

        try:
            result = scaleImage(orig_data,
                                direction=direction,
                                height=height,
                                width=width,
                                **parameters)
        except (ConflictError, KeyboardInterrupt):
            raise
        except Exception:
            exception('could not scale "%r" of %r',
                      orig_value, self.context.absolute_url())
            return
        if result is not None:
            data, format, dimensions = result
            mimetype = 'image/%s' % format.lower()
            value = orig_value.__class__(
                data, contentType=mimetype, filename=orig_value.filename)
            value.fieldname = fieldname
            return value, format, dimensions

    def image_format(self,fieldname='image'):
#         import pdb
#         pdb.set_trace()
        orig_value = getattr(self.context, fieldname)
        if orig_value is None:
            return "jpg"        
        format = orig_value.contentType.split('/', 1)[1]
        return format        


    def scale(self,
              fieldname=None,
              scale=None,
              height=None,
              width=None,
              direction='thumbnail',
              **parameters):
#         import pdb
#         pdb.set_trace()
        if fieldname is None:

            
            fieldname = IPrimaryFieldInfo(self.context).fieldname
        if scale is not None:
            available = self.getAvailableSizes(fieldname)
            if not scale in available:
                return None
            width, height = available[scale]

        if self.request is not None:
            alsoProvides(self.request, IDisableCSRFProtection)

        storage = AnnotationStorage(self.context, self.modified)
        info = storage.scale(factory=self.create,
                             fieldname=fieldname,
                             height=height,
                             width=width,
                             direction=direction,
                             **parameters)

        if info is not None:
            info['fieldname'] = fieldname
            scale_view = ImageScale(self.context, self.request, **info)
            return scale_view.__of__(self.context)

