# -*- coding: utf-8 -*-
from zope.interface.common import mapping
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveSAConnectLayer(IDefaultBrowserLayer):
    """Browserlayer
    """


class ISQLAlchemyConnectionStrings(mapping.IMapping):
    """A collection of SQLAlchemy connection strings"""
