# -*- coding: utf-8 -*-
from collective.saconnect import MessageFactory as _
from collective.saconnect.interfaces import ISQLAlchemyConnectionStrings
from plone.app.z3cform.layout import wrap_form
from plone.z3cform.crud import crud
from Products.CMFCore.interfaces import ISiteRoot
from zope import schema
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface


class IConnectionLine(Interface):
    """One row in the form
    """
    connname = schema.ASCIILine(
        title=_(u'label_connection_name', default=u'Connection name'),
        description=_(u'description_connection_name', default=u''),
        required=True,
    )
    connstring = schema.ASCIILine(
        title=_(u"label_connection_string",
                default=u"SQLAlchemy connection string"),
        description=_(u"description_connection_string",
                      default=u"driver://user:password@hostname/database"),
        required=True,
        default="sqlite:///"
    )


@implementer(IConnectionLine)
class ConnectionLine(object):

    def __init__(self, name, string, form):
        self._connname = name
        self._connstring = string
        self._form = form

    @property
    def connname(self):
        return self._connname

    @connname.setter
    def connname(self, name):
        name = name.strip()
        if name == self._connname:
            return

        storage = self._form.storage
        del storage[self._connname]
        storage[name] = self.connstring
        self._connname = name

    @property
    def connstring(self):
        return self._connstring

    @connstring.setter
    def connstring(self, string):
        string = string.strip()
        if string == self._connstring:
            return

        storage = self._form.storage
        storage[self.connname] = self._connstring = string


class SQLAlchemyConnectionsForm(crud.CrudForm):
    label = _(u'label_saconnectform', u'Manage SQLAlchemy connection strings')
    update_schema = IConnectionLine

    def __init__(self, context, request):
        crud.CrudForm.__init__(self, context, request)
        self.storage = ISQLAlchemyConnectionStrings(
            getUtility(ISiteRoot)
        )

    def get_items(self):
        names = self.storage.keys()
        names.sort()
        return [(name, ConnectionLine(name, self.storage[name], self))
                for name in names]

    def add(self, data):
        name = data['connname'].strip()
        if str(name) in self.storage:
            msg = _(u'error_name_already_registered',
                    u'The connection name is already registered')
            msg = translate(msg, self.request)
            raise schema.ValidationError(msg)

        self.storage[name] = data['connstring'].strip()
        return ConnectionLine(name, data['connstring'].strip(), self)

    def remove(self, (id, item)):
        del self.storage[item.connname]

SQLAlchemyConnectionsView = wrap_form(SQLAlchemyConnectionsForm)
