from vk.methods import Messages, Account, Apps, AppWidgets, Auth, Board, Database, Docs, Fave, Friends, Gifts, Groups, Leads, Likes, Market
from vk.utils import ContextInstanceMixin


class API(ContextInstanceMixin):
    def __init__(self, vk):
        self.vk = vk

        self.account = Account(vk, category="account")
        self.messages = Messages(vk, category="messages")
        self.apps = Apps(vk, category="apps")
        self.appwidgets = AppWidgets(vk, category="appwidgets")
        self.auth = Auth(vk, category="auth")
        self.board = Board(vk, category="board")
        self.database = Database(vk, category="database")
        self.docs = Docs(vk, category="docs")
        self.fave = Fave(vk, category="fave")
        self.friends = Friends(vk, category="friends")
        self.gifts = Gifts(vk, category="gifts")
        self.groups = Groups(vk, category="groups")
        self.leads = Leads(vk, category="leads")
        self.likes = Likes(vk, category="likes")
        self.market = Market(vk, category="market")
