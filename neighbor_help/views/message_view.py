from flask import Blueprint, request, session
from ..repositorys.props import auth, success, error, panic
from ..models import User, Message
from .. import db
from ..config import Config
from ..services.tool import base_query, get_user_info
from datetime import datetime
import json


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


# ###########需修改  # 已修改
@message_view.route("/linlidai/release", methods=["POST"])
@panic()
def linlidai_release():
    data = request.get_json()

    print(data["img_path"])
    if data["img_path"][0:4] == "http":
        img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][11:])
    elif data["img_path"][0:6] == "wxfile":
        img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][9:])

    content = {}
    content["img_url"] = img_url
    content["get_method"] = data["get_method"]
    content["mass_list"] = data["mass_list"]

    message = Message()
    message.user_id = data["user_id"]
    message.message_type = 3    # 邻里代
    message.message_name = data["type_id"]
    message.title = data["address"]
    message.content = json.dumps(content)
    message.time = datetime.now()

    db.session.add(message)
    db.session.commit()

    return success()


@message_view.route("/linlidai/list", methods=["GET"])
@panic()
def linlidai_list():
    type_id = request.args.get("type_id")
    
    result = []
    messages = base_query(Message).filter_by(message_type=3, message_name=type_id).order_by(Message.time.desc()).all()
    for message in messages:
        content = json.loads(message.content)
        result.append({
            "id": message.id,
            "user_info": get_user_info(message.user_id),
            "message_type": message.message_type,
            "message_name": message.message_name,
            "address": message.title,
            "img_url": content["img_url"],
            "get_method": content["get_method"],
            "mass_list": content["mass_list"],
            "time": str(message.time)
        })

    return success({
        "result": result
    })


# 根据message_id获得message
@message_view.route("/linlidai/single", methods=["GET"])
@panic()
def linlidai_single():
    message_id = request.args.get("message_id")

    result = {}
    message = base_query(Message).filter_by(id=message_id).first()
    if message is not None:
        content = json.loads(message.content)
        result["id"] = message.id
        result["user_info"] = get_user_info(message.user_id)
        result["message_type"] = message.message_type
        result["message_name"] = message.message_name
        result["address"] = message.title
        result["img_url"] = content["img_url"]
        result["get_method"] = content["get_method"]
        result["mass_list"] = content["mass_list"]
        result["time"] = str(message.time)

    return success({
        "result": result
    })
    

@message_view.route("/linliyue/release", methods=["POST"])
@panic()
def linliyue_release():
    data = request.get_json()

    print(data["img_path"])
    if data["img_path"][0:4] == "http":
        img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][11:])
    elif data["img_path"][0:6] == "wxfile":
        img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][9:])

    content = {}
    content["img_url"] = img_url
    content["one_input"] = data["one_input"]
    content["two_input"] = data["two_input"]
    content["three_input"] = data["three_input"]

    message = Message()
    message.user_id = data["user_id"]
    message.message_type = 2    # 邻里约
    message.message_name = data["type_id"]
    message.title = data["title"]
    message.content = json.dumps(content)
    message.time = datetime.now()

    db.session.add(message)
    db.session.commit()

    return success()


@message_view.route("/linliyue/list", methods=["GET"])
@panic()
def linliyue_list():
    type_id = request.args.get("type_id")
    
    result = []
    messages = base_query(Message).filter_by(message_type=2, message_name=type_id).order_by(Message.time.desc()).all()
    for message in messages:
        content = json.loads(message.content)
        result.append({
            "id": message.id,
            "user_info": get_user_info(message.user_id),
            "message_type": message.message_type,
            "message_name": message.message_name,    # 这里指大分类type下的小分类type，前端用不到
            "img_url": content["img_url"],
            "one_input": content["one_input"],
            "two_input": content["two_input"],
            "three_input": content["three_input"],
            "time": str(message.time)
        })

    return success({
        "result": result
    })


# 根据message_id获得message
@message_view.route("/linliyue/single", methods=["GET"])
@panic()
def linliyue_single():
    message_id = request.args.get("message_id")

    result = {}
    message = base_query(Message).filter_by(id=message_id).first()
    if message is not None:
        content = json.loads(message.content)
        result["id"] = message.id
        result["user_info"] = get_user_info(message.user_id)
        result["message_type"] = message.message_type
        result["message_name"] = message.message_name    # 前端用不到
        result["title"] = message.title
        result["img_url"] = content["img_url"]
        result["one_input"] = content["one_input"]
        result["two_input"] = content["two_input"]
        result["three_input"] = content["three_input"]
        result["time"] = str(message.time)

    return success({
        "result": result
    })