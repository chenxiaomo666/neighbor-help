# coding:utf-8

from .. import db

"""
对于邻里代购，超过一定年龄的老人每个月有两张免费的代金券，不用则清零
年轻人可以领取代购任务获得代金券用于发布代购信息（每周日清零）
老年人不能领取代购任务，
没有代金券发布一次任务四元钱，从账户余额扣除
"""


class Voucher(db.Model):
    __tablename__ = 'voucher'

    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer)
    voucher_type = db.Column("voucher_type", db.Integer)  # 0:邻里代购
    acquire_time = db.Column("acquire_time", db.DateTime)
    is_delete = db.Column("is_delete", db.Integer)
