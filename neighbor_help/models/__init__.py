from .. import db, app
from .user import User
from .voucher import Voucher
from .message import Message


def init_model():
    db.create_all(app=app)