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


# 根据business_id获得相对应的name，用于前端页面展示
@message_view.route("/message/name", methods=["GET"])
@panic()
def message_name():
    message_type = request.args.get("business_id")
    return success({
        "message_name": id_name[int(message_type)]
    })


# 邻里享模块发布物品或车位共享信息，insert
@message_view.route("/linlixaing/release", methods=["POST"])
@panic()
def linlixiang_release():
    data = request.get_json()
    try:
        img_url = ""
        if data["img_path"][0:4] == "http":
            img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][11:])
        elif data["img_path"][0:6] == "wxfile":
            img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][9:])
    except:
        img_url = ""
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


# 根据share_type获取共享信息列表
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


# 单个信息详情展示
@message_view.route("/linlixiang/single", methods=["GET"])
@panic()
def linlixiang_single():
    message_id = request.args.get("message_id")
    result = {}
    message = base_query(Message).filter_by(id=message_id).first()
    if message is not None:
        result["user_info"] = get_user_info(message.user_id)
        result["time"] = str(message.time)
        if message.message_name == "物品共享":
            result["title"] = message.message_name
            result["name"] = message.title
            result["img_url"] = message.content
        elif message.message_name == "车位共享":
            result["title"] = message.message_name
            result["avail_time"] = message.title
            result["img_url"] = message.content
    return success({
        "result": result
    })


# ###########需修改  # 已修改  邻里代模块发布信息
@message_view.route("/linlidai/release", methods=["POST"])
@panic()
def linlidai_release():
    data = request.get_json()
    try:
        img_url = ""
        if data["img_path"][0:4] == "http":
            img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][11:])
        elif data["img_path"][0:6] == "wxfile":
            img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][9:])
    except:
        img_url = ""
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


# 根据type_id获得发布内容简要列表
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


# 根据message_id获得message详细信息
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

############################################
@message_view.route("/linliyue/release", methods=["POST"])
@panic()
def linliyue_release():
    data = request.get_json()

    try:
        img_url = ""
        if data["img_path"][0:4] == "http":
            img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][11:])
        elif data["img_path"][0:6] == "wxfile":
            img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][9:])
    except:
        img_url = ""

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


##########################
@message_view.route("/dynamic/release", methods=["POST"])
@panic()
def dynamic_release():
    data = request.get_json()

    print(data)

    try:
        img_url = ""
        if data["img_path"][0:4] == "http":
            img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][11:])
        elif data["img_path"][0:6] == "wxfile":
            img_url = "https://dev.mylwx.cn:5000/file/{}".format(data["img_path"][9:])
    except:
        img_url = ""

    content = {}
    content["img_url"] = img_url
    content["content"] = data["content"]

    message = Message()
    message.user_id = data["user_id"]
    message.message_type = 9    # 邻里动态
    message.message_name = "邻里动态"
    # message.title = data["title"]
    message.content = json.dumps(content)
    message.time = datetime.now()

    db.session.add(message)
    db.session.commit()

    return success()


@message_view.route("/dynamic/list", methods=["GET"])
@panic()
def dynamic_list():
    
    result = []
    messages = base_query(Message).filter_by(message_type=9).order_by(Message.time.desc()).all()
    for message in messages:
        content = json.loads(message.content)
        result.append({
            "id": message.id,
            "user_info": get_user_info(message.user_id),
            "img_url": content["img_url"],
            "content": content["content"],
            "time": str(message.time)
        })

    return success({
        "result": result
    })


# 给用户发消息
@message_view.route("/news/send", methods=["POST"])
@panic()
def news_send():

    data = request.get_json()
    from_user = get_user_info(data["user_id"])
    target_user = get_user_info(data["target_user_id"])
    print(data)
    message_time = data["time"]

    if data["type"] == "邻里约":
        news_content = "{}向您在邻里约中{}时提出的标题为{}，内容为{}的活动发起了加入请求".format(from_user["name"], message_time,  data["title"], data["content"])
    elif data["type"] == "邻里代":
        news_content = "{}向您在邻里代中{}时提出的地址为{}，代购内容为{}的请求发起了接单".format(from_user["name"], message_time, data["address"], data["mass_list"])
    elif data["type"] == "邻里享":
        if data["title"] == "物品共享":
            news_content = "{}向您在邻里享中{}时分享的名为{}的物品很感兴趣，提出了申请".format(from_user["name"], message_time, data["name"])
        elif data["title"] == "车位共享":
            news_content = "{}向您在邻里享中{}时分享的，可用时间在{}的车位很感兴趣，提出了申请".format(from_user["name"], message_time, data["avail_time"])

    store_content = {}
    store_content["news_content"] = news_content
    store_content["from_user"] = from_user
    store_content["target_user"] = target_user
    store_content["message_time"] = message_time
    store_content["message_id"] = data["message_id"]

    message = Message()
    message.user_id = data["target_user_id"]
    message.message_type = 100   # 额，储存该推送消息是否被阅读过
    message.message_name = "最近消息"
    message.content = json.dumps(store_content)
    message.time = datetime.now()

    db.session.add(message)
    db.session.commit()

    return success()


@message_view.route("/news/list", methods=["GET"])
@panic()
def news_list():
    user_id = request.args.get("user_id")
    is_read = request.args.get("is_read")

    result = []
    messages = base_query(Message).filter_by(user_id=user_id, message_type=is_read).all()
    for message in messages:
        store_content = json.loads(message.content)
        result.append({
            "message_id": message.id,
            "news_content": store_content["news_content"],
            "time" : message.time,
            "from_user": store_content["from_user"],
            "is_read": is_read
        })

    return success({
        "result": result
    })


@message_view.route("/news/toread", methods=["post"])
@panic()
def news_to_read():
    data = request.get_json()
    message_id = data["message_id"]
    
    message = base_query(Message).filter_by(id=message_id).first()
    if message is not None:
        message.message_type = 101

        db.session.commit()
        return success()
    else:
        return error(reason="message_id错误")


@message_view.route("/news/isjoin", methods=["get"])
@panic()
def news_is_join():
    user_id = request.args.get("user_id")
    message_id = request.args.get("message_id")

    result = 1
    messages = base_query(Message).filter_by(message_name="最近消息").all()
    for message in messages:
        store_content = json.loads(message.content)
        if (int(user_id) == store_content["from_user"]["user_id"]) and (message_id == store_content["message_id"]):
            result = 1
            break
    else:
        result = 0

    return success({
        "result": result
    })