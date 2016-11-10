# -*- coding: utf-8 -*-

from plone.dexterity.utils import iterSchemata
from plone.memoize.instance import memoize
from plone.rfc822 import constructMessageFromSchemata
from plone.rfc822 import renderMessage
from email.generator import Generator
import tempfile

@memoize
def _getStream(self):
        # We write to a TemporayFile instead of a StringIO because we don't
        # want to keep the full file contents around in memory, and because
        # this approach allows us to hand off the stream iterator to the
        # publisher, which will serve it efficiently even after the
        # transaction is closed
        out = tempfile.TemporaryFile(mode='w+b')
        generator = Generator(out, mangle_from_=False)        
#         generator.flatten(self._getMessage())
        generator.write(renderMessage(self._getMessage())[1:])        
        self._size = out.tell()
        out.seek(0)
        return out


    # internal helper methods

@memoize
def _getMessage(self):
        """Construct message on demand
        """
        message = constructMessageFromSchemata(
            self.context,
            iterSchemata(self.context)
        )

        # Store the portal type in a header, to allow it to be identifed later
#         message['Portal-Type'] = self.context.portal_type

        return message

