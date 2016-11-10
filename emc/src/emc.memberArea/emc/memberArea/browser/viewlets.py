# encoding=utf-8
from plone.app.layout.viewlets import common as base
from Products.CMFCore.permissions import ViewManagementScreens
from Products.CMFCore.utils import getToolByName
from emc.memberArea import DoFavorite
from emc.memberArea.interfaces import IFavoriting


class Favorite(base.ViewletBase):

    favorite = None
    is_manager = None
    can_favorite = None

    # Update methods are guaranteed to be called before rendering for
    # Viewlets and Portlets (Because they are IContentProvider objects)
    # and for z3c.forms and formlib forms. But *not* for normal Browser Pages
    def update(self):
        super(Favorite, self).update()

        if self.favorite is None:
            self.favorite = IFavoriting(self.context)

        if self.is_manager is None:
            self.pm = getToolByName(self.context, 'portal_membership')
            self.is_manager = self.pm.checkPermission(
                ViewManagementScreens, self.context)
            self.can_favorite = self.pm.checkPermission(
                DoFavorite, self.context)

    def favorited(self):
        "是否已被当前用户收藏,true:已被收藏"

        userid = self.pm.getAuthenticatedMember().getId()
        return not(self.favorite.favavailable(userid))

    def number(self):
        return self.favorite.number()

    def has_favorites(self):
        return (self.number() > 0)
