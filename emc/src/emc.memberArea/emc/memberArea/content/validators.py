# -*- coding: utf-8 -*-
from plone.namedfile.interfaces import INamedBlobFileField
# from plone.app.contenttypes.interfaces import IImage
from zope.interface import Invalid
from z3c.form import validator


# 1 MB size limit
MAXSIZE = 1024 * 1024


class FileSizeValidator(validator.FileUploadValidator):

    def validate(self, value):
        super(FileSizeValidator, self).validate(value)

        if value.getSize() > MAXSIZE:
            raise Invalid("File is too large (to many bytes)")


validator.WidgetValidatorDiscriminators(FileSizeValidator,
#                                        context=IImage,
                                        field=INamedBlobFileField)