"""
Easy to learn, fast to code, built on vk.py.
"""
from .dispatcher import Dispatcher
from .dispatcher.handler import SkipHandler
from .dispatcher.storage import Storage
from .middlewares.middlewares import BaseMiddleware
from .rules import rules
from .rules.rules import BaseRule
from .rules.rules import NamedRule
