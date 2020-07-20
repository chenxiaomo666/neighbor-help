from sqlalchemy import or_
from ..models import User, Voucher
from ..config import Config
from .. import db
import datetime


def base_query(model):
    """
    所有未被删除的记录
    """
    return model.query.filter(or_(model.is_delete.is_(None), model.is_delete == 0))


def get_user_info(user_id):

    user = base_query(User).filter_by(id=user_id).first()
    if user is None:
        return {}
    else:
        return {
            "user_id": user.id,
            "name": user.name,
            "age": user.age,
            "balance": user.balance,   # 账户余额
            "address": user.address,
            "phone": user.phone,
            "openid": user.openid,
            "nickname": user.nickname,
            "head_img": user.head_img,
            "sex": user.sex
        }


# 检查用户是否有钱或者代金券可以发布邻里代购资格，如果有资格，就扣除相应代金券或者金钱
def release(user_id):
    user = base_query(User).filter_by(id=user_id).first()
    if user is None:
        raise Exception("无法定位用户信息")
    
    voucher = base_query(Voucher).filter_by(user_id=user.id).first()
    if voucher is None:    # 用户没有代金券了，只能用钱购买
        if user.balance < 4:   # 用户账户余额低于四元，不能发起
            return False
        else:
            user.balance = user.balance-4   # 扣除四元
            db.session.commit()
            return True
    else:
        voucher.is_delete = 1
        db.session.commit()
        return True


# 系统之初运行函数，用于增加和清除代金券
def voucher_check():
    now = datetime.datetime.now()
    users = base_query(User).all()
    for user in users:
        if user.age >= Config.RETIREMENT:   # 老人
            # 检查是否需要清除代金券
            vouchers = base_query(Voucher).filter_by(user_id=user.id).all()
            for voucher in vouchers:
                acquire_time = voucher.acquire_time
                if acquire_time.year <= now.year and acquire_time.month < now.month:
                    voucher.is_delete = 1
            db.session.commit()
                
            # 检查本月是否给老人发放过代金券
            voucher = Voucher.query.filter_by(user_id=user.id).all()
            if voucher == []:  # 代表本月没有发放代金券
                for i in range(2):
                    voucher = Voucher()
                    voucher.user_id = user.id
                    voucher.voucher_type = 0   # 0代表是邻里代购的消费券
                    voucher.acquire_time = now
                    db.session.add(voucher)
                db.session.commit()
            else:
                acquire_time = voucher[-1].acquire_time
                if acquire_time.year == now.year and acquire_time.month < now.month:
                    for i in range(2):
                        voucher = Voucher()
                        voucher.user_id = user.id
                        voucher.voucher_type = 0   # 0代表是邻里代购的消费券
                        voucher.acquire_time = now
                        db.session.add(voucher)
                    db.session.commit()
        else:   # 不是老人
            # 检查是否需要清空青年人的消费券
            weekday = now.weekday()
            sunday_time = now+datetime.timedelta(days=-weekday)
            vouchers = base_query(Voucher).filter_by(user_id=user.id).all()
            for voucher in vouchers:
                acquire_time = voucher.acquire_time
                if acquire_time.year <= sunday_time.year and (acquire_time.month <= sunday_time.month and acquire_time.day < sunday_time.day) :
                    voucher.is_delete = 1
            db.session.commit()

    return 0
                
            


