# -*- coding: utf-8 -*-
from collective.saconnect.interfaces import ISQLAlchemyConnectionStrings
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import XMLAdapterBase
from zope import component

FILENAME = 'saconnections.xml'


class SQLAlchemyConnectionStringsXMLAdapter(XMLAdapterBase):
    """XML im- and exporter for SQLAlchemy Connection strings"""
    component.adapts(ISQLAlchemyConnectionStrings, ISetupEnviron)

    _LOGGER_ID = 'collective.saconnect'

    def _exportNode(self):
        node = self._doc.createElement('connections')
        names = self.context.keys()
        names.sort()

        for name in names:
            child = self._doc.createElement('connection')
            child.setAttribute('name', name)
            child.setAttribute('string', self.context[name])
            node.appendChild(child)

        self._logger.info('Exported: %s' % ', '.join(names))
        return node

    def _importNode(self, node):
        if self.environ.shouldPurge():
            self.context.clear()
            self._logger.info('Connection strings purged.')

        imported = []
        for child in node.childNodes:
            if child.nodeName == 'connection':
                name = child.getAttribute('name').encode('ascii')
                if child.hasAttribute('remove'):
                    if name in self.context:
                        del self.context[name]
                    continue

                conn = child.getAttribute('string').encode('ascii')
                self.context[name] = conn
                imported.append(name)
        if imported:
            self._logger.info('Imported: %s' % ', '.join(imported))


def importConnections(context):
    data = context.readDataFile(FILENAME)
    if not data:
        return

    storage = ISQLAlchemyConnectionStrings(context.getSite())
    importer = component.queryMultiAdapter((storage, context), IBody)
    if importer:
        importer.body = data


def exportConnections(context):
    storage = ISQLAlchemyConnectionStrings(context.getSite())
    exporter = component.queryMultiAdapter((storage, context), IBody)
    if exporter:
        data = exporter.body
        if data is not None:
            context.writeDataFile(FILENAME, data, exporter.mime_type)
