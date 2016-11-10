from zope.publisher.browser import BrowserPage
from emc.memberArea.events import FavoriteEvent,UnFavoriteEvent
from zope.event import notify
# from emc.memberArea.interfaces import IFavoriting


class Favorite(BrowserPage):

    def __call__(self):

        notify(FavoriteEvent(self.context))
        return "success"


class UnFavorite(BrowserPage):

    def __call__(self):
        notify(UnFavoriteEvent(self.context))
        return "success"