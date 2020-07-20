# coding:utf-8

from .. import db


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer)
    message_type = db.Column("message_type", db.Integer)   # 消息类别
    message_name = db.Column("message_name", db.String(50))   # 类别名称
    title = db.Column("title", db.String(128))
    content = db.Column("content", db.Text)
    time = db.Column("time", db.DateTime)
    is_delete = db.Column("is_delete", db.Integer)
