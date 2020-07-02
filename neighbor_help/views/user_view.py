from flask import Blueprint, request, session
from ..repositorys.props import auth, success, error, panic
from ..models import User
from .. import db
from ..config import Config
from ..services.tool import base_query, get_user_info
import requests
import json

user_view = Blueprint("user_view", __name__)


# 增加新用户，实现user_id与微信号一一绑定
@user_view.route("/user/add", methods=["POST"])
@panic()
def user_add():
    user_data = request.get_json()
    user = base_query(User).filter_by(openid=user_data['openid']).first()
    if user is None:
        user = User()
    user.name = user_data["name"]
    user.openid = user_data["openid"]
    user.nickname = user_data["nickname"]
    user.head_img = user_data["head_img"]
    user.sex = user_data["sex"]
    user.phone = user_data["phone"]
    user.address = user_data["address"]

    db.session.add(user)
    db.session.flush()

    session["user_id"] = user.id

    db.session.commit()

    return success()


# 查询微信用户是否在本数据库中进行过绑定
@user_view.route("/user/query", methods=["GET"])
@panic()
def user_query():
    data = dict(request.args)
    data.update({
        "appid": Config.APPID,
        "secret": Config.SECRET,
    })

    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = data

    response = requests.get(url=url, params=params)
    user_data = json.loads(response.text)

    user_openid = user_data['openid']

    user = base_query(User).filter_by(openid=user_openid).first()
    if user is not None:
        is_bind = True
        session["user_id"] = user.id
    else:
        is_bind = False

    return success({
        "is_bind": is_bind,
        "open_id": user_openid
    })


