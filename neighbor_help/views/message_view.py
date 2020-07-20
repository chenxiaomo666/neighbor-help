from flask import Blueprint, request, session
from ..repositorys.props import auth, success, error, panic
from ..models import User, Message
from .. import db
from ..config import Config
from ..services.tool import base_query, get_user_info
from datetime import datetime


message_view = Blueprint("message_view", __name__)

id_name = {
        1: "邻里享",
        2: "邻里约",
        3: "邻里代",
        4: "邻里教",
        5: "邻里宠",
        6: "邻里务",
        7: "邻里团",
        8: "邻里帮",
        9: "邻里抗灾"
    }


# 获取指定message_type列表
@message_view.route("/message/list", methods=["GET"])
@panic()
def message_list():
    message_type = request.args.get("business_id")

    result = []
    messages = base_query(Message).filter_by(message_type=message_type).order_by(Message.time.desc()).all()
    for message in messages:
        result.append({
            "id": message.id,
            "user_info": get_user_info(message.user_id),
            "message_type": message.message_type,
            "message_name": message.message_name,
            "title": message.title,
            "content": message.content,
            "time": str(message.time)
        })

    return success({
        "result": result
    })


# 添加message
@message_view.route("/message/add", methods=["POST"])
@panic()
def message_add():
    data = request.get_json()
    
    message = Message()
    message.user_id = data["user_id"]
    message.message_type = data["business_id"]
    message.message_name = id_name[int(data["business_id"])]
    message.title = data["title"]
    message.content = data["content"]
    message.time = datetime.now()

    db.session.add(message)
    db.session.commit()

    return success()


@message_view.route("/message/name", methods=["GET"])
@panic()
def message_name():
    message_type = request.args.get("business_id")

    return success({
        "message_name": id_name[int(message_type)]
    })


@message_view.route("/linlixaing/release", methods=["POST"])
@panic()
def linlixiang_release():
    data = request.get_json()

    print(data["img_path"])
    if data["img_path"][0:4] == "http":
        img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][11:])
    elif data["img_path"][0:6] == "wxfile":
        img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][9:])

    message = Message()
    message.user_id = data["user_id"]
    message.message_type = 1    # 邻里享
    message.message_name = data["share_name"]
    if data["share_name"] == "物品共享":
        message.title = data["mess_name"]
    elif data["share_name"] == "车位共享":
        message.title = "{}|{}".format(data["start_time"], data["end_time"])
    message.content = img_url
    message.time = datetime.now()

    db.session.add(message)
    db.session.commit()

    return success()


@message_view.route("/linlixiang/list", methods=["GET"])
@panic()
def linlixiang_list():
    share_type = request.args.get("share_type")
    share_name = ""
    if share_type == "1":
        share_name = "物品共享"
    elif share_type == "2":
        share_name = "车位共享"
    result = []
    messages = base_query(Message).filter_by(message_type=1, message_name=share_name).order_by(Message.time.desc()).all()
    for message in messages:
        result.append({
            "id": message.id,
            "user_info": get_user_info(message.user_id),
            "message_type": message.message_type,
            "message_name": message.message_name,
            "mess_name": message.title,
            "img_url": message.content,
            "time": str(message.time)
        })

    return success({
        "result": result
    })