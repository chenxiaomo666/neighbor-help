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
@user_view.route("/user/upsert", methods=["POST"])
@panic()
def user_add():
    user_data = request.get_json()
    if user_data.get("user_id") is None:
        user = base_query(User).filter_by(openid=user_data['openid']).first()
        if user is None:
            user = User()
        user.name = user_data["name"]
        user.head_img = user_data["head_img"]
        user.phone = user_data["phone"]
        user.age = user_data["age"]
        user.address = user_data["address"]
        user.openid = user_data["openid"]
        user.nickname = user_data["nickname"]
        user.sex = user_data["sex"]
        db.session.add(user)
    else:
        if user_data["img_change"]==1:
            print(user_data["head_img"])
            if user_data["head_img"][0:4] == "http":
                img_url = "https://dev.mylwx.cn:5000/file/{}".format(user_data["head_img"][11:])
            elif data["head_img"][0:6] == "wxfile":
                img_url = "https://dev.mylwx.cn:5000/file/{}".format(user_data["head_img"][9:])
        else:
            img_url = user_data["head_img"]

        user_id = user_data.get("user_id")
        user = base_query(User).filter_by(id=user_id).first()
        user.name = user_data["name"]
        user.head_img = img_url
        user.phone = user_data["phone"]
        user.age = user_data["age"]
        user.address = user_data["address"]
    db.session.flush()

    # session["user_id"] = user.id

    db.session.commit()

    return success({
        "user_id": user.id
    })


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
        user_id = user.id
        print("用户已绑定", session.get("user_id"))
    else:
        is_bind = False
        user_id = None

    return success({
        "is_bind": is_bind,
        "open_id": user_openid,
        "user_id": user_id
    })


# 查询微信用户是否在本数据库中进行过绑定
@user_view.route("/user/info", methods=["GET"])
@panic()
def user_info():
    user_id = request.args.get("user_id")

    result = get_user_info(user_id)

    return success({
        "result": result
    })