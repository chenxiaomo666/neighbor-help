from sqlalchemy import or_
from ..models import User


def base_query(model):
    """
    所有未被删除的记录
    """
    return model.query.filter(or_(model.is_delete.is_(None), model.is_delete == 0))


def get_user_info(user_id):
    result = {}
    user = base_query(User).filter_by(id=user_id).first()
    if user is None:
        return result
    else:
        result = {
            "user_id": user.id,
            "name": user.name,
            "address": user.address,
            "phone": user.phone,
            "openid": user.openid,
            "nickname": user.nickname,
            "head_img": user.head_img,
            "sex": user.sex
        }

