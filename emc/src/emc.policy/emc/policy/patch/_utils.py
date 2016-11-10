"""Implementation of IMessageAPI methods.

import these from plone.rfc822 directly, not from this module.

See interfaces.py for details.
"""

import logging
from cStringIO import StringIO

# Note: We use capitalised module names to be compatible with Python 2.4
from email.Message import Message 
from email.Header import Header, decode_header
from email.Generator import Generator

from zope.component import queryMultiAdapter
from zope.schema import getFieldsInOrder

from plone.rfc822.interfaces import IFieldMarshaler
from plone.rfc822.interfaces import IPrimaryField

LOG = logging.getLogger('plone.rfc822')



def constructMessage(context, fields, charset='utf-8'):
    msg = Message()
    
    primary = []
    
    # First get all headers, storing primary fields for later
    for name, field in fields:
        
        if IPrimaryField.providedBy(field):
            primary.append((name, field,))
            break
        
#         marshaler = queryMultiAdapter((context, field,), IFieldMarshaler)
#         if marshaler is None:
#             LOG.debug("No marshaler found for field %s of %s" % (name, repr(context)))
#             continue
#          
#         try:
#             value = marshaler.marshal(charset, primary=False)
#         except ValueError, e:
#             LOG.debug("Marshaling of %s for %s failed: %s" % (name, repr(context), str(e)))
#             continue
#          
#         if value is None:
#             value = ''
#         elif not isinstance(value, str):
#             raise ValueError("Marshaler for field %s did not return a string" % name)
#          
#         if marshaler.ascii and '\n' not in value:
#             msg[name] = value
#         else:
#             msg[name] = Header(value, charset)
    
    # Then deal with the primary field
    
    # If there's a single primary field, we have a non-multipart message with
    # a string payload

    if len(primary) == 1:
        name, field = primary[0]
        
        marshaler = queryMultiAdapter((context, field,), IFieldMarshaler)
#         import pdb
#         pdb.set_trace()
        if marshaler is not None:
            contentType = marshaler.getContentType()
            payloadCharset = marshaler.getCharset(charset)
            
#             if contentType is not None:
#                 msg.set_type(contentType)
#             
#             if payloadCharset is not None:
#                 # using set_charset() would also add transfer encoding,
#                 # which we don't want to do always
#                 msg.set_param('charset', payloadCharset)
                
            value = marshaler.marshal(charset, primary=True)
#             import pdb
#             pdb.set_trace()
            if value is not None:
                msg.set_payload(value)
            
#             marshaler.postProcessMessage(msg)
    
    # Otherwise, we return a multipart message
    
    elif len(primary) > 1:
        msg.set_type('multipart/mixed')
        
        for name, field in primary:
            
            marshaler = queryMultiAdapter((context, field,), IFieldMarshaler)
            if marshaler is None:
                continue
            
            payload = Message()
            attach = False
            
            contentType = marshaler.getContentType()
            payloadCharset = marshaler.getCharset(charset)
            
            if contentType is not None:
                payload.set_type(contentType)
                attach = True
            if payloadCharset is not None:
                # using set_charset() would also add transfer encoding,
                # which we don't want to do always
                payload.set_param('charset', payloadCharset)
                attach = True
            
            value = marshaler.marshal(charset, primary=True)
            
            if value is not None:
                payload.set_payload(value)
                attach = True
            
            if attach:
                marshaler.postProcessMessage(payload)
                msg.attach(payload)

    return msg


